from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from difflib import get_close_matches
from pathlib import Path

import tomlkit
from pydantic import BaseModel, ValidationError

from . import (
    ConfigFileAlreadyExistsError,
    ConfigFileNotFoundError,
    ConfigT,
    ConfigValidationError,
    ConfigValidationIssue,
)


@dataclass
class _TomlSourceIndex:
    """Maps TOML key paths to line numbers for validation error reporting."""

    path_lines: dict[tuple[str | int, ...], int] = field(default_factory=dict)
    container_keys: dict[tuple[str | int, ...], dict[str, int]] = field(
        default_factory=dict
    )

    @classmethod
    def from_content(cls, content: str) -> _TomlSourceIndex:
        index = cls()
        current_container: tuple[str | int, ...] = ()
        array_counts: dict[tuple[str, ...], int] = {}

        for line_number, raw_line in enumerate(content.splitlines(), start=1):
            stripped = raw_line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            if stripped.startswith("[[") and stripped.endswith("]]"):
                table_path = tuple(cls._parse_key_path(stripped[2:-2].strip()))
                item_index = array_counts.get(table_path, 0)
                array_counts[table_path] = item_index + 1
                current_container = table_path + (item_index,)
                index.path_lines[current_container] = line_number
                continue

            if stripped.startswith("[") and stripped.endswith("]"):
                current_container = tuple(cls._parse_key_path(stripped[1:-1].strip()))
                index.path_lines[current_container] = line_number
                continue

            if "=" not in stripped:
                continue

            key_text = stripped.split("=", 1)[0].strip()
            key_path = tuple(cls._parse_key_path(key_text))
            if not key_path:
                continue

            full_path = current_container + key_path
            index.path_lines[full_path] = line_number
            index.container_keys.setdefault(current_container, {})[
                key_path[-1]
            ] = line_number

        return index

    @staticmethod
    def _parse_key_path(text: str) -> list[str]:
        parts: list[str] = []
        current: list[str] = []
        quote: str | None = None

        for character in text:
            if quote is not None:
                if character == quote:
                    quote = None
                else:
                    current.append(character)
                continue

            if character in {'"', "'"}:
                quote = character
                continue

            if character == ".":
                part = "".join(current).strip()
                if part:
                    parts.append(part)
                current = []
                continue

            current.append(character)

        part = "".join(current).strip()
        if part:
            parts.append(part)
        return parts

    def resolve(self, loc: tuple[str | int, ...]) -> tuple[int | None, str | None]:
        """Resolve a pydantic error location to a TOML line number."""
        if loc in self.path_lines:
            source_key = next(
                (part for part in reversed(loc) if isinstance(part, str)), None
            )
            return self.path_lines[loc], source_key

        if loc:
            container = loc[:-1]
            container_line = self.path_lines.get(container)
            field_name = loc[-1]
            if isinstance(field_name, str):
                sibling_key = self._find_close_key(
                    field_name,
                    self.container_keys.get(container, {}),
                )
                if sibling_key is not None:
                    return self.container_keys[container][sibling_key], sibling_key
            return container_line, None

        return None, None

    @staticmethod
    def _find_close_key(field_name: str, known_keys: dict[str, int]) -> str | None:
        """Fuzzy-match a field name against known TOML keys."""
        matches = get_close_matches(field_name, known_keys, n=1, cutoff=0.75)
        if matches:
            return matches[0]
        return None


def _format_loc(loc: tuple[str | int, ...]) -> str:
    """Format a pydantic error location tuple as a human-readable path."""
    parts: list[str] = []
    for part in loc:
        if isinstance(part, int):
            if parts:
                parts[-1] = f"{parts[-1]}[{part}]"
            else:
                parts.append(f"[{part}]")
            continue
        parts.append(part)
    return ".".join(parts)


class TomlHandler:
    """Load and save pydantic config models as TOML files."""

    @classmethod
    def load(cls, path: Path, config_type: type[ConfigT]) -> ConfigT:
        """Load one pydantic config model from a TOML file."""
        try:
            content = path.read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise ConfigFileNotFoundError(
                f"config file does not exist: {path}"
            ) from exc

        data = tomllib.loads(content)
        source_index = _TomlSourceIndex.from_content(content)

        try:
            return config_type.model_validate(data)
        except ValidationError as exc:
            issues: list[ConfigValidationIssue] = []
            for error in exc.errors():
                loc = tuple(error["loc"])
                line, source_key = source_index.resolve(loc)
                issues.append(
                    ConfigValidationIssue(
                        loc=loc,
                        field_path=_format_loc(loc),
                        message=str(error["msg"]),
                        line=line,
                        source_key=source_key,
                    )
                )
            raise ConfigValidationError(path, issues, exc) from exc

    @classmethod
    def save(cls, path: Path, config: BaseModel, *, overwrite: bool = True) -> Path:
        """Write one pydantic config model to a TOML file."""
        if path.exists() and not overwrite:
            raise ConfigFileAlreadyExistsError(f"config file already exists: {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            tomlkit.dumps(config.model_dump(mode="python")), encoding="utf-8"
        )
        return path
