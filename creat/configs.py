import json
from pathlib import Path
from typing import Type, TypeVar

from json_source_map import calculate  # type: ignore
from pydantic import BaseModel, Field, ConfigDict
from pydantic_core import ValidationError


class ShellRun(BaseModel):
    """Single run in system default shell shell."""

    text: str = Field(..., description="Text to execute in system default shell.")


class SampleConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    runs: list[ShellRun] = Field(
        default_factory=list,
        description="""List of runs to execute after scaffold instantiation is made.""",
        min_items=1,  # type: ignore
    )


class ScaffoldConfig(BaseModel):
    """Project local config."""

    sample: SampleConfig = Field(default_factory=SampleConfig)


class GlobalConfig(BaseModel):
    scaffold_config_name: str = Field(
        ".creat.json",
        description="Name of project local creat config file",
    )


__global_config: GlobalConfig | None = None


def set_global_config(config: GlobalConfig) -> GlobalConfig:
    global __global_config
    __global_config = config
    return __global_config


def get_global_config() -> GlobalConfig:
    global __global_config
    if __global_config is None:
        raise ValueError("Global config not set")
    return __global_config


T_Model = TypeVar("T_Model", bound=BaseModel)


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
            data = json.load(fo)
            return Model(**data)
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
