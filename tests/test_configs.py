from pathlib import Path

import pytest

from creat.configs import (
    Config,
    ConfigNotInitializedError,
    ConfigValidationError,
    format_config,
    get_config,
    init_config,
    load_config,
)
from creat.configs.access import ConfigSlot
from creat.configs.toml import TomlHandler


def test_config_slot_requires_init() -> None:
    slot: ConfigSlot[Config] = ConfigSlot()

    with pytest.raises(ConfigNotInitializedError):
        slot.get()


def test_config_slot_returns_set_config() -> None:
    slot: ConfigSlot[Config] = ConfigSlot()
    config = Config(config_path=Path("/tmp/creat.toml"), project_system="ai-agents")

    assert slot.set(config) is config
    assert slot.get() is config


def test_toml_handler_loads_config_defaults(tmp_path: Path) -> None:
    config_path = tmp_path / "creat.toml"
    config_path.write_text("", encoding="utf-8")

    config = TomlHandler.load(config_path, Config)

    assert config.project_system == "ai-agents"


def test_toml_handler_reports_location_for_invalid_config(tmp_path: Path) -> None:
    config_path = tmp_path / "creat.toml"
    config_path.write_text(
        "# comment\n\nproject_system = 1\n",
        encoding="utf-8",
    )

    with pytest.raises(ConfigValidationError) as exc_info:
        TomlHandler.load(config_path, Config)

    assert exc_info.value.issues
    assert exc_info.value.issues[0].field_path == "project_system"
    assert exc_info.value.issues[0].line == 3


def test_toml_handler_loads_config_values(tmp_path: Path) -> None:
    config_path = tmp_path / "creat.toml"
    config_path.write_text('project_system = "from-toml"\n', encoding="utf-8")

    config = TomlHandler.load(config_path, Config)

    assert config.project_system == "from-toml"


def test_load_config_uses_selected_path_for_missing_file(tmp_path: Path) -> None:
    config_path = tmp_path / "creat.toml"

    config = load_config(config_path)

    assert config.config_path == config_path
    assert config.project_system == "ai-agents"


def test_load_config_uses_default_user_config_when_present(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config_path = tmp_path / "creat.toml"
    config_path.write_text('project_system = "from-file"\n', encoding="utf-8")
    monkeypatch.setattr("creat.configs.config.DEFAULT_CONFIG_PATH", config_path)

    config = load_config()

    assert config.config_path == config_path
    assert config.project_system == "from-file"


def test_init_config_makes_active_config_available(tmp_path: Path) -> None:
    config_path = tmp_path / "creat.toml"

    config = init_config(config_path)

    assert get_config() is config


def test_format_config_uses_toml_for_toml_paths(tmp_path: Path) -> None:
    config = Config(
        config_path=tmp_path / "creat.toml",
        project_system="from-toml",
    )

    text = format_config(config)

    assert 'config_path = "' in text
    assert 'project_system = "from-toml"' in text
