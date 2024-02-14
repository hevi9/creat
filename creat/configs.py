from pydantic import BaseModel, Field


class ShellRun(BaseModel):
    """Single run in system default shell shell."""

    text: str = Field(..., description="Text to execute in system default shell.")


class SampleConfig(BaseModel):
    runs: list[ShellRun] = Field(
        default_factory=list,
        description="""List of runs to execute after scaffold instantiation is made.""",
    )


class LocalConfig(BaseModel):
    """Project local config."""

    sample: SampleConfig = Field(default_factory=SampleConfig)


class GlobalConfig(BaseModel):
    local_config_name: str = Field(
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
