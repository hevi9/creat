from rich import print

from . import app
from .scaffolds import index


@app.command("list")
def cmd_list():
    """List scaffolds."""
    scaffolds = index()
    for scaffold in scaffolds.values():
        print(scaffold.id, scaffold.root)
