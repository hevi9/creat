import sys
from pathlib import Path
from typing import Collection, Iterable, List, Optional, Set

import typer
from loguru import logger
from rich.live import Live
from rich.table import Table

from creat.models.files import File

from . import get_console, setup_logger
from .builds import build_index
from .indexes import Index

app = typer.Typer()


# remove logger not to interfere with shell completion, add loggers later on setup
# interferes with pytest logging
# logger.remove()


class _State:
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
            cls._index = build_index(roots, ignore_globs)
        return cls._index


def _tidy(text: str) -> str:
    return " ".join(text.split())


def _tags_complete(ctx: typer.Context, incomplete: str) -> Collection[str]:
    try:
        if ctx.parent is not None:
            index = _State.get_index(roots=ctx.parent.params.get("roots"))
        else:
            index = _State.get_index()
        tags_given = set(ctx.params["tags"])
        yield from _tags_complete_real(tags_given, incomplete, index)
    except Exception as ex:
        yield f"Completion error: {repr(ex)}"


def _tags_complete_real(
    tags_given: Set[str],
    tag_incomplete: str,
    index: Index,
) -> Collection[str]:
    for tag in index.get_tags(tags_given):
        if tag.startswith(tag_incomplete):
            yield tag


# def name_complete_remains(names: Union[Iterable[str], Sized]) -> Iterable[str]:
#     index = _State.get_index().index
#     if not names:
#         return set(index.keys())
#     names = set(names)
#     reduced = set()
#     for name in names:
#         for source in index.getall(name):
#             reduced.add(source)
#     remains = set()
#     for source in reduced:
#         if names.issubset(source.tags):
#             remains.update(source.tags - names)
#     return remains


# @app.command("new")
# def cmd_new(
#     source: str = typer.Argument(
#         ...,
#         help="Source name.",
#         # autocompletion=_source_completion,
#     ),
#     target: str = typer.Argument(
#         ...,
#         help="Target directory or file name. May not exists.",
#     ),
# ):
#     """Make new target from given source."""
#     try:
#         index = _State.get_index()
#         source_use = index.find(source)
#         context = make_root_context(target)
#         validate(context)
#         source_use.run(context)
#     except Exception as ex:
#         get_console().print_exception()
#         raise typer.Exit(1) from ex


# @app.command("develop")
# def cmd_develop(
#     source: str = typer.Argument(
#         ...,
#         help="Source to develop",
#     ),
#     target: Path = typer.Argument(
#         ...,
#         help="Temporary target directory",
#     ),
# ):
#     """Develop sources."""
#     try:
#         if target.exists():
#             raise FileExistsError(f"{str(target)}: already exists !")
#         index = _State.get_index()
#         src = index.find(source)
#         logger.debug(
#             "source={}, target={}, source-path={}",
#             source,
#             target,
#             src.location.path_root,
#         )
#         for changes in watch(src.location.path_root):
#             logger.debug("changes: {}", changes)
#             logger.debug("Creating new development target instance")
#             time.sleep(3.0)
#             logger.debug("done")
#     except Exception as ex:
#         get_console().print_exception()
#         raise typer.Exit(1) from ex


@app.command("list")
def cmd_list(
    tags: List[str] = typer.Argument(
        None,
        autocompletion=_tags_complete,
        help="Sources to list.",
    ),
):
    """List sources."""
    logger.debug("sources: {}", tags)
    try:
        index = _State.get_index()

        def view():
            sources_result = []
            if not tags:
                sources_result = index.sources
            else:
                for source in index.sources:
                    for key in tags:
                        for source_key in source.tags:
                            if source_key.startswith(key):
                                sources_result.append(source)
            table = Table(box=None)
            table.add_column("Source")
            table.add_column("Doc")
            table.add_column("Root")
            table.add_column("Path")
            for source in sorted(sources_result, key=lambda s: s.name):
                table.add_row(
                    source.name,
                    source.doc,
                    str(source.location.path_root),
                    str(source.location.path_rel),
                )
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
    _State.roots = roots
    setup_logger(level="TRACE" if debug else "INFO")
    logger.debug("roots: {}", roots)


if __name__ == "__main__":
    app()
