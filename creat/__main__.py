import sys
import time
from pathlib import Path
from typing import Iterable, List, Optional

import typer
from loguru import logger
from rich.live import Live
from rich.table import Table
from watchgod import watch

from . import get_console, setup_logger
from .builds import build
from .contexts import make_root_context, validate
from .index import Index
from .schema import File

app = typer.Typer()


# remove logger not to interfere with shell completion, add loggers later on
# setup
logger.remove()


class _state:
    roots: List[Path] = []
    ignore_globs: List[str] = [".git"]
    _index: Optional[Index] = None

    @classmethod
    def get_index(
        cls,
        roots: Optional[Iterable[Path]] = None,
        ignore_globs: Optional[Iterable[str]] = None,
    ) -> Index:
        roots = roots or []
        ignore_globs = ignore_globs or []
        roots = set(cls.roots + list(roots))
        ignore_globs = set(cls.ignore_globs + list(ignore_globs))
        if not cls._index:
            cls._index = build(roots, ignore_globs)
        return cls._index


def _tidy(text: str) -> str:
    return " ".join(text.split())


def _source_completion(ctx: typer.Context, incomplete: str):
    try:
        # get roots definition from main context
        index = _state.get_index(roots=ctx.parent.params.get("roots"))
        # logger.debug(
        #     "index={}, params={}, parent.params={}",
        #     index,
        #     ctx.params,
        #     ctx.parent.params,
        # )
        valid_completion_items = [(s.sid, s.doc) for s in index.sources.values()]
        if not valid_completion_items:
            raise ValueError(f"{index} empty")
        names = ctx.params.get("source") or []
        for name, help_text in valid_completion_items:
            if name.startswith(incomplete) and name not in names:
                yield name, help_text
    except Exception:
        logger.add("creat_completion.log")
        logger.exception("Can't make completion")


@app.command("new")
def cmd_new(
    source: str = typer.Argument(
        ...,
        help="Source name.",
        autocompletion=_source_completion,
    ),
    target: str = typer.Argument(
        ...,
        help="Target directory or file name. May not exists.",
    ),
):
    """Make new target from given source."""
    try:
        index = _state.get_index()
        source_use = index.find(source)
        context = make_root_context(target)
        validate(context)
        source_use.run(context)
    except Exception as ex:
        get_console().print_exception()
        raise typer.Exit(1) from ex


@app.command("develop")
def cmd_develop(
    source: str = typer.Argument(
        ...,
        help="Source to develop",
    ),
    target: Path = typer.Argument(
        ...,
        help="Temporary target directory",
    ),
):
    """Develop sources."""
    try:
        if target.exists():
            raise FileExistsError(f"{str(target)}: already exists !")
        index = _state.get_index()
        src = index.find(source)
        logger.debug(
            "source={}, target={}, source-path={}",
            source,
            target,
            src.location.path_root,
        )
        for changes in watch(src.location.path_root):
            logger.debug("changes: {}", changes)
            logger.debug("Creating new development target instance")
            time.sleep(3.0)
            logger.debug("done")
    except Exception as ex:
        get_console().print_exception()
        raise typer.Exit(1) from ex


@app.command("list")
def cmd_list(
    sources: List[str] = typer.Argument(
        None,
        autocompletion=_source_completion,
        help="Sources to list.",
    ),
):
    """List sources."""
    logger.debug("sources: {}", sources)
    try:
        index = _state.get_index()

        def view():
            table = Table(box=None)
            table.add_column("Source")
            table.add_column("Doc")
            for source in sorted(index.sources.values(), key=lambda s: s.sid):
                show = True
                if sources and not any(source.sid.startswith(s) for s in sources):
                    show = False
                if show and source.show:
                    table.add_row(source.sid, source.doc)
            return table

        with Live(console=get_console(), auto_refresh=False) as live:
            live.update(view(), refresh=False)
    except Exception as ex:
        get_console().print_exception()
        raise typer.Exit(1) from ex


@app.command("json-schema")
def cmd_json_schema(
    path: Optional[Path] = typer.Argument(
        None,
        help="File to write json schema",
    )
):
    """Generate json schema."""
    file = sys.stdout
    if path:
        file = path.open("wt", encoding="utf-8")
    print(File.schema_json(), file=file)
    file.close()


@app.callback()
def main(
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Enable debug logging.",
    ),
    roots: List[Path] = typer.Option(
        [Path("~").expanduser() / ".creat"],
        "--root",
        envvar="CREATROOTS",
        help=_tidy(
            """Roots to find sources. Can be given multiple times.
            Environment variable CREATROOTS can be used also to
            define source paths. """
        ),
    ),
):
    _state.roots = roots
    logger.debug("roots: {}", roots)
    setup_logger(level="TRACE" if debug else "INFO")


if __name__ == "__main__":
    app()
