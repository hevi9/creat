from rich import print

from . import app
from .scaffolds import build_index


@app.command("list")
def cmd_list():
    """List scaffolds."""
    scaffolds = build_index()
    for scaffold in scaffolds.values():
        print(scaffold.id, scaffold.root)
