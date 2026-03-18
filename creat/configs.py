import json
import tomllib
from contextvars import ContextVar
from pathlib import Path
from typing import Any, Generic, Type, TypeVar

import tomli_w
from json_source_map import calculate  # type: ignore
from pydantic import BaseModel, Field
from pydantic_core import ValidationError

T_Model = TypeVar("T_Model", bound=BaseModel)
DEFAULT_CONFIG_PATH = Path("~/.config/creat/creat.json").expanduser()


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


def _normalize_config_path(path: Path | str) -> Path:
    return Path(path).expanduser()


def _uses_toml(path: Path) -> bool:
    return path.suffix.lower() == ".toml"


def _build_validation_locations(
    path: Path,
    error: ValidationError,
    source_map: dict[str, Any] | None = None,
) -> list[ErrorLocation]:
    locations = []
    for item in error.errors():
        location_path = list(item["loc"])
        error_context_path = None
        if source_map is not None:
            while location_path:
                try:
                    pointer = "/" + "/".join([str(part) for part in location_path])
                    error_context_path = source_map[pointer]
                    break
                except KeyError:
                    location_path.pop()
                    continue

        error_location = ErrorLocation(
            subject=str(item["loc"][-1]) if item["loc"] else "",
            msg=item["msg"],
        )
        if error_context_path is not None:
            line = error_context_path.value_end.line
            column = error_context_path.value_end.column
            error_location.location = f"{path!s}:{line}:{column}"
            error_location.line = line
            error_location.column = column
        locations.append(error_location)
    return locations


def json_to_obj(path: Path | str, Model: Type[T_Model]) -> T_Model:
    config_path = _normalize_config_path(path)
    text = config_path.read_text(encoding="utf-8")
    try:
        return Model.model_validate_json(text)
    # todo JSONDecodeError: Expecting ',' delimiter: line 10 column 1 (char 87)
    except ValidationError as ex:
        source_map = calculate(text)
        locations = _build_validation_locations(config_path, ex, source_map)
        raise ValidationLocationError(
            f"Validation errors on {config_path!s}", error=ex, locations=locations
        )


def toml_to_obj(path: Path | str, Model: Type[T_Model]) -> T_Model:
    config_path = _normalize_config_path(path)
    text = config_path.read_text(encoding="utf-8")
    data = tomllib.loads(text)
    try:
        return Model.model_validate(data)
    except ValidationError as ex:
        locations = _build_validation_locations(config_path, ex)
        raise ValidationLocationError(
            f"Validation errors on {config_path!s}", error=ex, locations=locations
        )


def file_to_obj(path: Path | str, Model: Type[T_Model]) -> T_Model:
    config_path = _normalize_config_path(path)
    if _uses_toml(config_path):
        return toml_to_obj(config_path, Model)
    return json_to_obj(config_path, Model)


def default_config(config_path: Path = DEFAULT_CONFIG_PATH) -> Config:
    return Config(config_path=config_path, project_system="ai-agents")


def load_config(config_path: Path | str | None = None) -> Config:
    selected_path = DEFAULT_CONFIG_PATH
    if config_path is not None:
        selected_path = _normalize_config_path(config_path)

    try:
        config = file_to_obj(selected_path, Config)
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
    if _uses_toml(config.config_path):
        return tomli_w.dumps(payload).rstrip("\n") + "\n"
    return json.dumps(payload, indent=2) + "\n"


def write_config(config: Config) -> Path:
    config_path = _normalize_config_path(config.config_path)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(format_config(config), encoding="utf-8")
    return config_path
