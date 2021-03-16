""" mk CLI. """

# pylint: disable=redefined-builtin
# pylint: disable=unexpected-keyword-arg, no-value-for-parameter


import sys
from pathlib import Path

import click
from rich.table import Table

from .find import update_index_from_roots
from .index import Index
from .run import run
from .ui import console, ui
from .validate import validate


@click.group()
@click.option(
    "--verbose",
    type=click.BOOL,
    default=True,
    help="Show verbose messages.",
    show_default=True,
)
@click.option(
    "paths",
    "--path",
    default=[Path("~").expanduser() / ".mkroot"],
    multiple=True,
    envvar="MKPATH",
    type=click.Path(),
    help="""
        Path(s) to find sources. Can be given multiple times. Environment
        variable MKPATH can be used also to define source paths
    """,
    show_default=True,
)
@click.pass_context
def cli(ctx, verbose, paths):
    """ TODO: cli description """
    ctx.ensure_object(dict)
    ui.is_verbose = verbose
    ctx.obj["paths"] = paths


@cli.command()
@click.argument("source_name")
@click.argument("target_name")
@click.pass_context
def new(ctx, source_name, target_name):
    """ Make new target from given source. """
    paths = ctx.obj["paths"]
    try:
        index = Index()
        update_index_from_roots(index, paths, [])
        ui.talk(
            "Have {num} sources in {paths}",
            num=len(index.sources),
            paths=",".join(str(p) for p in paths),
        )
        source = index.find(source_name)
        context = {
            "name": target_name,
            "target": target_name,
        }
        validate(context)
        run(source, context)
    except KeyError as ex:
        ui.error_exit("Source not found {ex}", ex=ex)
    except Exception as ex:
        console.print_exception()
        ui.error_exit("{ex}", ex=ex)


@cli.command()
@click.pass_context
def list(ctx):
    """ List sources. """
    paths = ctx.obj["paths"]
    try:
        index = Index()
        update_index_from_roots(index, paths, [])
        ui.talk(
            "Have {num} sources in {paths}",
            num=len(index.sources),
            paths=",".join(str(p) for p in paths),
        )
        table = Table(box=None)
        table.add_column("Source")
        table.add_column("Description")
        for source in sorted(index.sources, key=lambda s: s.id2):
            if source.show:
                table.add_row(source.id, source.doc)
        console.print(table)
    except Exception as ex:
        ui.error_exit("{ex}", ex=ex)


if __name__ == "__main__":
    # pylint: disable=unexpected-keyword-arg, no-value-for-parameter
    cli(prog_name="{} -m {}".format(sys.executable, __package__))
