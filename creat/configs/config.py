from pathlib import Path

import tomlkit
from pydantic import BaseModel, Field

from creat.configs import ConfigFileNotFoundError
from creat.configs.access import ConfigSlot
from creat.configs.toml import TomlHandler

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


# Reason: process-global config slot for the active session.
config_slot: ConfigSlot[Config] = ConfigSlot[Config]()


def _normalize_config_path(path: Path | str) -> Path:
    return Path(path).expanduser()


def default_config(config_path: Path = DEFAULT_CONFIG_PATH) -> Config:
    return Config(config_path=config_path, project_system="ai-agents")


def load_config(config_path: Path | str | None = None) -> Config:
    selected_path = DEFAULT_CONFIG_PATH
    if config_path is not None:
        selected_path = _normalize_config_path(config_path)

    try:
        config = TomlHandler.load(selected_path, Config)
    except ConfigFileNotFoundError:
        config = default_config(selected_path)

    # Reason: the selected path stays authoritative for the active session,
    # even when the config file does not exist yet.
    config.config_path = selected_path
    return config


def init_config(config_path: Path | str | None = None) -> Config:
    return config_slot.set(load_config(config_path), config_source="init_config")


def get_config() -> Config:
    return config_slot.get()


def format_config(config: Config) -> str:
    payload = config.model_dump(mode="json")
    return tomlkit.dumps(payload).rstrip("\n") + "\n"


def write_config(config: Config) -> Path:
    config_path = _normalize_config_path(config.config_path)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(format_config(config), encoding="utf-8")
    return config_path
