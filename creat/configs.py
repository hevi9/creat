from pathlib import Path
from typing import Generic, Type, TypeVar

from json_source_map import calculate  # type: ignore
from pydantic import BaseModel, Field
from pydantic_core import ValidationError

T_Model = TypeVar("T_Model", bound=BaseModel)


class UserConfig(BaseModel):
    user_config_path: Path = Field(
        Path("~/.config/creat/creat.json").expanduser(),
        description="User config file path.",
    )
    project_system: str = Field(
        "ai-agents",
        description="Active project creation system.",
    )


class ConfigAccess(Generic[T_Model]):
    _config: T_Model | None = None

    def init(self, config: T_Model) -> T_Model:
        self._config = config
        return self._config

    def __call__(self) -> T_Model:
        if self._config is None:
            raise RuntimeError("Config is not initialized.")
        return self._config


x_user_config: ConfigAccess[UserConfig] = ConfigAccess[UserConfig]()


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


def json_to_obj(path: Path | str, Model: Type[T_Model]) -> T_Model:
    try:
        with open(path, "r", encoding="utf-8") as fo:
            return Model.model_validate_json(fo.read())
    # todo JSONDecodeError: Expecting ',' delimiter: line 10 column 1 (char 87)
    except ValidationError as ex:
        with open(path, "r", encoding="utf-8") as fo:
            text = fo.read()
        source_map = calculate(text)
        locations = []
        for error in ex.errors():
            # todo implement dict up tracking when exact pointer is not found
            location_path = list(error["loc"])
            error_context_path = None
            while location_path:
                try:
                    pointer = "/" + "/".join([str(i) for i in location_path])
                    error_context_path = source_map[pointer]
                    break
                except KeyError:
                    location_path.pop()
                    continue
            error_location = ErrorLocation(
                subject=str(error["loc"][-1]),
                msg=error["msg"],
            )
            if error_context_path is not None:
                line = error_context_path.value_end.line
                column = error_context_path.value_end.column
                error_location.location = f"{path!s}:{line}:{column}"
                error_location.line = line
                error_location.column = column
            locations.append(error_location)
        raise ValidationLocationError(
            f"Validation errors on {path!s}", error=ex, locations=locations
        )
