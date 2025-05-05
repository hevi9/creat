import typer
from rich import print

from ..scaffolds import build_index

cli = typer.Typer()


@cli.command("list")
def list_():
    """List scaffolds."""
    scaffolds = build_index()
    for scaffold in scaffolds.values():
        print(scaffold.id, scaffold.root)
