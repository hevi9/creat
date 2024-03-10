from pathlib import Path

from copier import Worker

from . import app

from typer import Argument, Option

from .scaffolds import build_index

from rich import print


@app.command("new")
def cmd_new(
    source: str = Argument(
        help="Scaffold source name.",
    ),
    target: Path = Argument(
        help="Target path.",
    ),
    dry_run: bool = Option(
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
