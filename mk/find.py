""" Find mk roots and files from file system. """

# TODO: move objects to build.py

# pylint: disable=undefined-loop-variable

from pathlib import Path
from typing import Iterable

from .build import make_sources_from_file_yaml
from .index import Index
from .location import Location
from .source import Source

MK_GLOB = ("*.mk.yaml", "*.mk.yml")


def find_mk_files(mkpaths: Iterable[Path], ignores: Iterable[str]) -> Iterable[Location]:
    """ Find mk files from mk paths, skipping ignores. """

    def traverse(path_rel):
        path_abs = root / path_rel
        if path_abs.is_dir():
            for entry in path_abs.glob("*"):
                for ignore_glob in ignores:
                    if entry.match("**/" + ignore_glob):
                        continue
                yield from traverse(path_rel / entry.name)
        elif path_abs.is_file():
            for glob in MK_GLOB:
                if path_abs.match("**/" + glob):
                    yield Location(path_root=root, path_rel=path_rel)

    for root in mkpaths:
        yield from traverse(Path("."))


def find_mk_sources_from_roots(
    mkroots: Iterable[Path],
    ignores: Iterable[str],
) -> Iterable[Source]:
    """Build sources from mk files in gives mk roots.

    Top level function.
    """
    for location in find_mk_files(mkroots, ignores):
        yield from make_sources_from_file_yaml(location)


def update_index_from_roots(
    index: Index,
    roots: Iterable[Path],
    ignore: Iterable[str],
) -> None:
    """Update index sources from given root paths. Ignore given
    ignore patterns in tree traversing.

    :param index: Index to update.
    :param roots: Directory root paths to traverse and seek sources.
    :param ignore:  ignore patterns to ignore in tree traversing.
    """
    for source in find_mk_sources_from_roots(roots, ignore):
        index.add_source(source)
    for source in index.sources:
        source.update(index)
