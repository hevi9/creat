from pathlib import Path
from typing import Annotated, Optional

import typer

from . import __version__
from .cmd import config
from .configs import Config, x_config, json_to_obj

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
    config_path: Path = typer.Option(
        Path("~/.config/creat/creat.json").expanduser(),
        help="Path to config.",
    ),
) -> None:
    """Load the active configuration."""
    try:
        config_data = json_to_obj(config_path, Config)
    except FileNotFoundError:
        config_data = Config()
    # Keep the selected path authoritative for the active session.
    config_data.config_path = config_path
    x_config.init(config_data)


if __name__ == "__main__":
    cli()
