""" mk CLI. """
import sys
from pathlib import Path
from typing import List, Optional

import typer
from rich.console import Console
from rich.table import Table

from creat.builds import update_index_from_roots
from creat.contexts import make_root_context, validate
from creat.schema import File

from . import get_console, setup_logger
from .index import Index
from .run import run

# from watchgod import awatch


app = typer.Typer()

_paths: List[Path]

_console: Console


def _tidy(text: str) -> str:
    return " ".join(text.split())


def _print_status(index, paths):
    pass
    # ui.talk(
    #     "Have {num} sources in {paths}",
    #     num=len(index.sources),
    #     paths=",".join(str(p) for p in paths),
    # )


@app.callback()
def main(
    debug: bool = typer.Option(
        False,
        help="Enable debug logging.",
    ),
    path: List[Path] = typer.Option(
        [Path("~").expanduser() / ".mkroot"],
        envvar="CREATPATH",
        help=_tidy(
            """Path(s) to find sources. Can be given multiple times.
            Environment variable MKPATH can be used also to
            define source paths """
        ),
    ),
):
    """Makes"""
    global _paths, _console
    _paths = path
    _console = get_console()
    setup_logger(level="TRACE" if debug else "INFO")


@app.command()
def new(
    source: str = typer.Argument(
        ...,
        help="Source name.",
    ),
    target: str = typer.Argument(
        ...,
        help="Target directory or file name. May not exists.",
    ),
):
    """Make new target from given source."""
    try:
        index = Index()
        update_index_from_roots(index, _paths, [])
        _print_status(index, _paths)
        source_use = index.find(source)
        context = make_root_context(target)
        validate(context)
        run(source_use, context)
    except KeyError as ex:
        _console.print_exception()
        raise typer.Exit(1) from ex
    except Exception as ex:
        _console.print_exception()
        raise typer.Exit(1) from ex


@app.command()
def list():  # pylint: disable=redefined-builtin
    """List sources."""
    try:
        index = Index()
        update_index_from_roots(index, _paths, [])
        # ui.talk(
        #     "Have {num} sources in {paths}",
        #     num=len(index.sources),
        #     paths=",".join(str(p) for p in CFG.paths),
        # )
        table = Table(box=None)
        table.add_column("Source")
        table.add_column("Description")
        for source in sorted(index.sources, key=lambda s: s.id):
            if source.show:
                table.add_row(source.id, source.doc)
        _console.print(table)
    except Exception as ex:
        _console.print_exception()
        raise typer.Exit(1) from ex


@app.command()
def develop(
    source: str = typer.Argument(
        ...,
        help="Source to develop",
    )
):
    """Develop sources."""
    # awatch()


@app.command()
def gen_json_schema(
    path: Optional[Path] = typer.Argument(
        None,
        help="File to write json schema",
    )
):
    """Generate json schema"""
    file = sys.stdout
    if path:
        file = path.open("wt", encoding="utf-8")
    print(File.schema_json(), file=file)
    file.close()


if __name__ == "__main__":
    app()
