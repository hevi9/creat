from dataclasses import dataclass
from contextvars import ContextVar
from pathlib import Path
from typing import Generic, Type, TypeVar

import tomlkit
from pydantic import BaseModel, Field
from pydantic_core import ValidationError
from tomlkit.items import Key
from tomlkit.parser import Parser

T_Model = TypeVar("T_Model", bound=BaseModel)
DEFAULT_CONFIG_PATH = Path("~/.config/creat/creat.toml").expanduser()


class Config(BaseModel):
    config_path: Path = Field(
        DEFAULT_CONFIG_PATH,
        description="Config file path.",
    )
    project_system: str = Field(
        "ai-agents",
        description="Active project creation system.",
    )


class ConfigAccess(Generic[T_Model]):
    def __init__(self, name: str = "config") -> None:
        # Reason: library code can run outside the Typer command chain,
        # so the active config needs a process-local access path.
        self._config: ContextVar[T_Model | None] = ContextVar(name, default=None)

    def init(self, config: T_Model) -> T_Model:
        self._config.set(config)
        return config

    def clear(self) -> None:
        self._config.set(None)

    def __call__(self) -> T_Model:
        config = self._config.get()
        if config is None:
            raise RuntimeError("Config is not initialized.")
        return config


x_config: ConfigAccess[Config] = ConfigAccess[Config]("creat_active_config")


class ErrorLocation(BaseModel):
    location: str = ""
    subject: str = ""
    msg: str
    line: int = 0
    column: int = 0


class ValidationLocationError(ValueError):
    error: ValidationError
    locations: list[ErrorLocation]

    def __init__(
        self, msg: str, error: ValidationError, locations: list[ErrorLocation]
    ) -> None:
        super().__init__(msg)
        self.error = error
        self.locations = locations


@dataclass(frozen=True)
class SourceLocation:
    line: int
    column: int


class TrackingParser(Parser):
    def __init__(self, string: str) -> None:
        super().__init__(string)
        self.path_locations: dict[tuple[str, ...], SourceLocation] = {}
        self._current_table_path: tuple[str, ...] = ()

    def _record_location(self, path: tuple[str, ...], location: SourceLocation) -> None:
        self.path_locations.setdefault(path, location)

    def _path_from_key(self, key: Key) -> tuple[str, ...]:
        return tuple(part.key for part in key)

    def _key_location(self) -> SourceLocation:
        with self._state(restore=True):
            while self._current.is_spaces():
                self.inc()
            line, column = self._src._to_linecol()

        return SourceLocation(line=line, column=column + 1)

    def _table_location(self) -> SourceLocation:
        with self._state(restore=True):
            self.inc()
            if self._current == "[":
                self.inc()
            while self._current.is_spaces():
                self.inc()
            line, column = self._src._to_linecol()

        return SourceLocation(line=line, column=column + 1)

    def _parse_key_value(self, parse_comment: bool = False):
        location = self._key_location()
        key, item = super()._parse_key_value(parse_comment=parse_comment)
        full_path = self._current_table_path + self._path_from_key(key)
        self._record_location(full_path, location)
        return key, item

    def _parse_table(self, parent_name=None, parent=None):
        _, key = self._peek_table()
        location = self._table_location()
        full_path = self._path_from_key(key)
        previous_path = self._current_table_path
        self._record_location(full_path, location)
        self._current_table_path = full_path
        try:
            return super()._parse_table(parent_name=parent_name, parent=parent)
        finally:
            self._current_table_path = previous_path


def _normalize_config_path(path: Path | str) -> Path:
    return Path(path).expanduser()


def _build_validation_locations(
    path: Path,
    error: ValidationError,
    source_map: dict[tuple[str, ...], SourceLocation] | None = None,
) -> list[ErrorLocation]:
    locations = []
    for item in error.errors():
        location_path = tuple(str(part) for part in item["loc"])
        error_context_path = None
        if source_map is not None:
            while location_path:
                try:
                    error_context_path = source_map[location_path]
                    break
                except KeyError:
                    location_path = location_path[:-1]
                    continue

        error_location = ErrorLocation(
            subject=str(item["loc"][-1]) if item["loc"] else "",
            msg=item["msg"],
        )
        if error_context_path is not None:
            line = error_context_path.line
            column = error_context_path.column
            error_location.location = f"{path!s}:{line}:{column}"
            error_location.line = line
            error_location.column = column
        locations.append(error_location)
    return locations


def toml_to_obj(path: Path | str, Model: Type[T_Model]) -> T_Model:
    config_path = _normalize_config_path(path)
    text = config_path.read_text(encoding="utf-8")
    # Reason: tomlkit keeps TOML parsing centralized, and the tracking parser
    # preserves source locations for later validation errors.
    parser = TrackingParser(text)
    data = parser.parse().unwrap()
    try:
        return Model.model_validate(data)
    except ValidationError as ex:
        locations = _build_validation_locations(config_path, ex, parser.path_locations)
        raise ValidationLocationError(
            f"Validation errors on {config_path!s}", error=ex, locations=locations
        )


def default_config(config_path: Path = DEFAULT_CONFIG_PATH) -> Config:
    return Config(config_path=config_path, project_system="ai-agents")


def load_config(config_path: Path | str | None = None) -> Config:
    selected_path = DEFAULT_CONFIG_PATH
    if config_path is not None:
        selected_path = _normalize_config_path(config_path)

    try:
        config = toml_to_obj(selected_path, Config)
    except FileNotFoundError:
        config = default_config(selected_path)

    # Reason: the selected path stays authoritative for the active session,
    # even when the config file does not exist yet.
    config.config_path = selected_path
    return config


def init_config(config_path: Path | str | None = None) -> Config:
    return x_config.init(load_config(config_path))


def get_config() -> Config:
    return x_config()


def format_config(config: Config) -> str:
    payload = config.model_dump(mode="json")
    return tomlkit.dumps(payload).rstrip("\n") + "\n"


def write_config(config: Config) -> Path:
    config_path = _normalize_config_path(config.config_path)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(format_config(config), encoding="utf-8")
    return config_path
