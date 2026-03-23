# Reason: creat entry point — fast file/project creation CLI (skeleton).
from typing import Annotated, Optional

import typer

from . import __version__

cli = typer.Typer(
    invoke_without_command=True,
    pretty_exceptions_enable=False,
    help="AI-agent project creation.",
)


def _version(value: bool) -> None:
    if value:
        typer.echo(f"creat {__version__}")
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
) -> None:
    """AI-agent project creation."""
    # Reason: skeleton has no subcommands yet — show help when invoked bare.
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())


if __name__ == "__main__":
    cli()
