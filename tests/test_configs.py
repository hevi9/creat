from pathlib import Path

import pytest

from creat.configs import (
    Config,
    ConfigAccess,
    ValidationLocationError,
    format_config,
    get_config,
    init_config,
    load_config,
    toml_to_obj,
)


def test_config_access_requires_init() -> None:
    access: ConfigAccess[Config] = ConfigAccess()

    with pytest.raises(RuntimeError):
        access()


def test_config_access_returns_initialized_config() -> None:
    access: ConfigAccess[Config] = ConfigAccess()
    config = Config(config_path=Path("/tmp/creat.toml"), project_system="ai-agents")

    assert access.init(config) is config
    assert access() is config


def test_toml_to_obj_loads_config_defaults(tmp_path: Path) -> None:
    config_path = tmp_path / "creat.toml"
    config_path.write_text("", encoding="utf-8")

    config = toml_to_obj(config_path, Config)

    assert config.project_system == "ai-agents"


def test_toml_to_obj_reports_location_for_invalid_config(tmp_path: Path) -> None:
    config_path = tmp_path / "creat.toml"
    config_path.write_text(
        "# comment\n\nproject_system = 1\n",
        encoding="utf-8",
    )

    with pytest.raises(ValidationLocationError) as exc_info:
        toml_to_obj(config_path, Config)

    assert exc_info.value.locations
    assert exc_info.value.locations[0].subject == "project_system"
    assert exc_info.value.locations[0].line == 3
    assert exc_info.value.locations[0].column == 1


def test_toml_to_obj_loads_config_values(tmp_path: Path) -> None:
    config_path = tmp_path / "creat.toml"
    config_path.write_text('project_system = "from-toml"\n', encoding="utf-8")

    config = toml_to_obj(config_path, Config)

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
    monkeypatch.setattr("creat.configs.DEFAULT_CONFIG_PATH", config_path)

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
