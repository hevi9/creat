from pathlib import Path

import typer
from copier import Worker
from rich import print

from ..scaffolds import build_index

cli = typer.Typer()


@cli.command("new")
def cmd_new(
    source: str = typer.Argument(
        help="Scaffold source name.",
    ),
    target: Path = typer.Argument(
        help="Target path.",
    ),
    dry_run: bool = typer.Option(
        False,
        help="Produce no real rendering.",
    ),
) -> None:
    """Instantiate files from scaffold."""
    index = build_index()
    scaffold = index[source]
    print(f"Creating new [yellow]{scaffold.root!s}[/yellow] to [green]{target}[/green]")
    worker = Worker(
        src_path=str(scaffold.root),
        dst_path=target,
        overwrite=False,
        skip_answered=False,
        pretend=dry_run,
    )
    worker.run_copy()
