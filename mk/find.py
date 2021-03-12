# pylint: disable=undefined-loop-variable

from pathlib import Path
from typing import Iterable

from .index import Index
from .location import Location
from .source import Source
from .build import make_sources_from_file_yaml

MK_GLOB = ("*.mk.yaml", "*.mk.yml")


def find_mk_files(mkpath: Iterable[Path], ignore: Iterable[str]) -> Iterable[Location]:
    def traverse(path_rel):
        path_abs = root / path_rel
        if path_abs.is_dir():
            for entry in path_abs.glob("*"):
                for ignore_glob in ignore:
                    if entry.match("**/" + ignore_glob):
                        continue
                yield from traverse(path_rel / entry.name)
        elif path_abs.is_file():
            for glob in MK_GLOB:
                if path_abs.match("**/" + glob):
                    yield Location(path_root=root, path_rel=path_rel)

    for root in mkpath:
        yield from traverse(Path("."))


def find_mk_sources_from_roots(
    roots: Iterable[Path], ignore: Iterable[str]
) -> Iterable[Source]:
    for location in find_mk_files(roots, ignore):
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
    for source in index.list():
        source.update(index)
