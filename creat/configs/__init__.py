from dataclasses import dataclass
from pathlib import Path
from typing import TypeVar

from pydantic import BaseModel, ValidationError


class ConfigNotInitializedError(RuntimeError):
    """Raised when config is accessed before startup initialization."""


class ConfigAlreadyInitializedError(RuntimeError):
    """Raised when config initialization is attempted more than once."""


class ConfigTypeMismatchError(RuntimeError):
    """Raised when a stored config does not match the requested type."""


class ConfigFileNotFoundError(FileNotFoundError):
    """Raised when a TOML config file does not exist."""


class ConfigFileAlreadyExistsError(FileExistsError):
    """Raised when a TOML config file exists and overwrite is disabled."""


@dataclass(frozen=True)
class ConfigValidationIssue:
    """One config validation issue enriched with source location metadata."""

    loc: tuple[str | int, ...]
    field_path: str
    message: str
    line: int | None = None
    source_key: str | None = None


class ConfigValidationError(ValueError):
    """Raised when a TOML config file fails schema validation."""

    def __init__(
        self,
        path: Path,
        issues: list[ConfigValidationIssue],
        validation_error: ValidationError,
    ) -> None:
        self.path = path
        self.issues = tuple(issues)
        self.validation_error = validation_error
        super().__init__(self._build_message())

    def _build_message(self) -> str:
        count = len(self.issues)
        noun = "error" if count == 1 else "errors"
        lines = [f"config validation failed with {count} {noun} in {self.path}"]
        for issue in self.issues:
            location = (
                f"line {issue.line}" if issue.line is not None else "unknown line"
            )
            lines.append(f"{location}: {issue.field_path}: {issue.message}")
        return "\n".join(lines)


ConfigT = TypeVar("ConfigT", bound=BaseModel)

# Reason: re-exports keep `from creat.configs import ...` working
# after the module-to-package migration.
from creat.configs.access import ConfigSlot  # noqa: E402
from creat.configs.config import (  # noqa: E402
    Config,
    DEFAULT_CONFIG_PATH,
    config_slot,
    default_config,
    format_config,
    get_config,
    init_config,
    load_config,
    write_config,
)
from creat.configs.toml import TomlHandler  # noqa: E402

__all__ = [
    "ConfigAlreadyInitializedError",
    "ConfigFileAlreadyExistsError",
    "ConfigFileNotFoundError",
    "ConfigNotInitializedError",
    "ConfigSlot",
    "ConfigT",
    "ConfigTypeMismatchError",
    "ConfigValidationError",
    "ConfigValidationIssue",
    "Config",
    "DEFAULT_CONFIG_PATH",
    "TomlHandler",
    "config_slot",
    "default_config",
    "format_config",
    "get_config",
    "init_config",
    "load_config",
    "write_config",
]
