# Reason: creatctl entry point — operations and admin CLI.
from pathlib import Path
from typing import Annotated, Optional

import typer

from creat import __version__
from creat.configs import init_config
from creat.configs.cli import config_validation_cli_handler
from creat.ctl import config

cli = typer.Typer(
    no_args_is_help=True,
    pretty_exceptions_enable=False,
    help="Operations and admin CLI for the creat system.",
)

cli.add_typer(config.cli)


def _version(value: bool) -> None:
    if value:
        typer.echo(f"creatctl {__version__}")
        raise typer.Exit(0)


@cli.callback()
def main(
    ctx: typer.Context,
    _version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            callback=_version,
            is_eager=True,
        ),
    ] = None,
    config_path: Annotated[
        Optional[Path],
        typer.Option(
            "--config",
            "--config-path",
            help=(
                "Path to the TOML config file. If omitted, the user config is "
                "loaded when present and defaults are used otherwise."
            ),
        ),
    ] = None,
) -> None:
    """Load the active configuration."""
    with config_validation_cli_handler():
        ctx.obj = init_config(config_path)


if __name__ == "__main__":
    cli()
