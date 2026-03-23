from typer.testing import CliRunner

from creat import __version__
from creat.__main__ import cli

runner = CliRunner()


def test_creat_version() -> None:
    result = runner.invoke(cli, ["--version"])

    assert result.exit_code == 0
    assert f"creat {__version__}" in result.stdout


def test_creat_help() -> None:
    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "AI-agent project creation" in result.stdout


def test_creat_no_args_shows_help() -> None:
    result = runner.invoke(cli, [])

    assert result.exit_code == 0
    assert "AI-agent project creation" in result.stdout
