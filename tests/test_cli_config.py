import json
from pathlib import Path

from typer.testing import CliRunner

from creat.__main__ import cli

runner = CliRunner()


def test_config_show_prints_active_config(tmp_path: Path) -> None:
    config_path = tmp_path / "creat.json"

    result = runner.invoke(cli, ["--config-path", str(config_path), "config", "show"])

    assert result.exit_code == 0
    config = json.loads(result.stdout)
    assert config["config_path"] == str(config_path)
    assert config["project_system"] == "ai-agents"


def test_config_init_writes_selected_path(tmp_path: Path) -> None:
    config_path = tmp_path / "creat.json"

    result = runner.invoke(cli, ["--config-path", str(config_path), "config", "init"])

    assert result.exit_code == 0
    assert result.stdout.strip() == f"Wrote {config_path}"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    assert config["config_path"] == str(config_path)
    assert config["project_system"] == "ai-agents"


def test_legacy_config_command_is_removed() -> None:
    result = runner.invoke(cli, ["config", "user"])

    assert result.exit_code != 0
    assert "No such command 'user'" in result.output


def test_legacy_config_path_option_is_removed(tmp_path: Path) -> None:
    config_path = tmp_path / "creat.json"

    result = runner.invoke(
        cli,
        ["--user-config-path", str(config_path), "config", "show"],
    )

    assert result.exit_code != 0
    assert "No such option: --user-config-path" in result.output
