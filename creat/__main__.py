from pathlib import Path
from typing import List

import typer

from creat.discovers import discover

from . import get_console, setup_logger


class _state:
    roots: List[Path] = []
    ignore_globs: List[str] = [".git"]


app = typer.Typer()


def _tidy(text: str) -> str:
    return " ".join(text.split())


# def _print_status(index, paths):
#     pass
#     # ui.talk(
#     #     "Have {num} sources in {paths}",
#     #     num=len(index.sources),
#     #     paths=",".join(str(p) for p in paths),
#     # )
#
#
#
#
# @app.command()
# def new(
#     source: str = typer.Argument(
#         ...,
#         help="Source name.",
#     ),
#     target: str = typer.Argument(
#         ...,
#         help="Target directory or file name. May not exists.",
#     ),
# ):
#     """Make new target from given source."""
#     try:
#         index = Index()
#         update_index_from_roots(index, _paths, [])
#         _print_status(index, _paths)
#         source_use = index.find(source)
#         context = make_root_context(target)
#         validate(context)
#         run(source_use, context)
#     except KeyError as ex:
#         _console.print_exception()
#         raise typer.Exit(1) from ex
#     except Exception as ex:
#         _console.print_exception()
#         raise typer.Exit(1) from ex
#
#
#
#
# @app.command()
# def develop(
#     source: str = typer.Argument(
#         ...,
#         help="Source to develop",
#     )
# ):
#     """Develop sources."""
#     # awatch()
#
#
# @app.command()
# def gen_json_schema(
#     path: Optional[Path] = typer.Argument(
#         None,
#         help="File to write json schema",
#     )
# ):
#     """Generate json schema"""
#     file = sys.stdout
#     if path:
#         file = path.open("wt", encoding="utf-8")
#     print(File.schema_json(), file=file)
#     file.close()
#
#


@app.command("list")
def cmd_list():
    """List sources."""
    locations = list(discover(_state.roots, _state.ignore_globs))
    get_console().print(locations)
    # try:
    #     index = Index()
    #     update_index_from_roots(index, _paths, [])
    #     # ui.talk(
    #     #     "Have {num} sources in {paths}",
    #     #     num=len(index.sources),
    #     #     paths=",".join(str(p) for p in CFG.paths),
    #     # )
    #     table = Table(box=None)
    #     table.add_column("Source")
    #     table.add_column("Description")
    #     for source in sorted(index.sources, key=lambda s: s.id):
    #         if source.show:
    #             table.add_row(source.id, source.doc)
    #     _console.print(table)
    # except Exception as ex:
    #     _console.print_exception()
    #     raise typer.Exit(1) from ex


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
    setup_logger(level="TRACE" if debug else "INFO")


if __name__ == "__main__":
    app()
