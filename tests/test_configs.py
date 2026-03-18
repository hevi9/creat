from pathlib import Path

import pytest

from creat.configs import Config, ConfigAccess, ValidationLocationError, json_to_obj


def test_config_access_requires_init() -> None:
    access: ConfigAccess[Config] = ConfigAccess()

    with pytest.raises(RuntimeError):
        access()


def test_config_access_returns_initialized_config() -> None:
    access: ConfigAccess[Config] = ConfigAccess()
    config = Config(config_path=Path("/tmp/creat.json"))

    assert access.init(config) is config
    assert access() is config


def test_json_to_obj_loads_config_defaults(tmp_path: Path) -> None:
    config_path = tmp_path / "creat.json"
    config_path.write_text("{}", encoding="utf-8")

    config = json_to_obj(config_path, Config)

    assert config.project_system == "ai-agents"


def test_json_to_obj_reports_location_for_invalid_config(tmp_path: Path) -> None:
    config_path = tmp_path / "creat.json"
    config_path.write_text('{"config_path": []}', encoding="utf-8")

    with pytest.raises(ValidationLocationError) as exc_info:
        json_to_obj(config_path, Config)

    assert exc_info.value.locations
    assert exc_info.value.locations[0].subject == "config_path"
