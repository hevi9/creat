from pathlib import Path
from typing import Annotated, Optional

import typer

from . import __version__
from .cmd import config
from .configs import UserConfig, x_user_config, json_to_obj

cli = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_enable=False,
    help="CLI foundation for the AI-agent project creation system.",
)

cli.add_typer(config.cli)


def _version(value: bool) -> None:
    if value:
        typer.echo(f"creat {__version__}")
        raise typer.Exit(0)


@cli.callback()
def main(
    _version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            callback=_version,
            is_eager=True,
        ),
    ] = None,
    user_config_path: Path = typer.Option(
        Path("~/.config/creat/creat.json").expanduser(),
        help="Path to user config.",
    ),
) -> None:
    """Load the active user configuration."""
    try:
        config_data = json_to_obj(user_config_path, UserConfig)
    except FileNotFoundError:
        config_data = UserConfig()
    config_data.user_config_path = user_config_path
    x_user_config.init(config_data)


if __name__ == "__main__":
    cli()
