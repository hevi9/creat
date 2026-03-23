# Reason: creat entry point — fast file/project creation CLI (skeleton).
from typing import Annotated, Optional

import subprocess

import typer

from . import __version__

PROMPT_TMPL = """
CREATE {args} AS {what} .
""".strip()

MODEL = "github-copilot/gpt-5.4"

cli = typer.Typer(
    invoke_without_command=True,
    pretty_exceptions_enable=False,
    help="AI-agent project creation.",
    no_args_is_help=True,
)


def _version(value: bool) -> None:
    if value:
        typer.echo(f"creat {__version__}")
        raise typer.Exit(0)


@cli.callback()
def main(
    ctx: typer.Context,
    what: Annotated[
        str,
        typer.Argument(
            ..., help="What to create (e.g. 'file', 'directory', 'project')"
        ),
    ],
    args: Annotated[
        list[str], typer.Argument(..., help="Arguments for the command")
    ] = [],
    _version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            callback=_version,
            is_eager=True,
        ),
    ] = None,
    as_files: Annotated[
        bool,
        typer.Option("-f", help="Output file paths instead of content"),
    ] = False,
    as_dirs: Annotated[
        bool,
        typer.Option("-d", help="Output directory paths instead of content"),
    ] = False,
    as_projects: Annotated[
        bool,
        typer.Option("-p", help="Output project paths instead of content"),
    ] = False,
) -> None:
    """AI-agent project creation."""
    # Reason: skeleton has no subcommands yet — show help when invoked bare.
    # if ctx.invoked_subcommand is None:
    #     typer.echo(ctx.get_help())

    match what:
        case "file":
            typer.echo(f"Creating file with args: {args}")
        case "directory":
            typer.echo(f"Creating directory with args: {args}")
        case "project":
            typer.echo(f"Creating project with args: {args}")
        case _:
            typer.echo(f"Unknown creation type: {what}")
            raise typer.Exit(1)
    prompt = PROMPT_TMPL.format(args=args, what=what)
    cargs = [
        "opencode",
        "--model",
        MODEL,
        "run",
        prompt,
    ]

    typer.echo(f"Prompt for AI agent:\n{cargs}")
    subprocess.run(cargs, check=True)


if __name__ == "__main__":
    cli()
