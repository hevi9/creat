""" Building source and action structure from .mk.yaml files. """

# pylint: disable=undefined-loop-variable

from __future__ import annotations

from pathlib import Path
from typing import Iterable

import strictyaml  # type: ignore

from . import MK_GLOB, get_console
from .action.copy import Copy
from .action.move import Move
from .action.remove import Remove
from .action.shell import Shell
from .action.use import Use
from .index import Index
from .location import Location
from .source import Source

MAKE_ITEM_MAP = {
    "shell": Shell,
    "use": Use,
    "remove": Remove,
    "copy": Copy,
    "move": Move,
}


def make_source_from_dict(item: dict, location: Location) -> Source:
    """Make source from given source control dict."""
    source = Source(
        name=item["source"],
        control=item,
        location=location,
    )
    make_list = item["make"]
    for make_item in make_list:
        if isinstance(make_item, str):
            make_item = {"shell": make_item}
        elif isinstance(make_item, dict):
            pass  # NOSONAR
        else:
            raise TypeError(f"Invalid make item type {type(make_item)}")
        make_type = make_item.keys() & MAKE_ITEM_MAP.keys()
        if len(make_type) < 1:
            raise ValueError(
                f"""Unknown make type in item {make_item} in {location},
                available make types {MAKE_ITEM_MAP.keys()}"""
            )
        if len(make_type) > 1:
            raise ValueError(f"Conflicting make types {make_type}")
        make_type = make_type.pop()
        source.make.append(MAKE_ITEM_MAP[make_type](source, make_item))  # type: ignore

    return source


def make_sources_from_file_yaml(location: Location) -> Iterable[Source]:
    """Make source item from yaml file."""
    console = get_console()
    with location.path_abs.open() as fo:
        text = fo.read()
        if text.strip() == "":
            console.print(f"{location} is empty, ignoring")
            return
        data = strictyaml.load(text, label=str(location.path_abs)).data
        if not isinstance(data, list):
            raise TypeError(f"Top content is not a list type: '{text}': {location}")
        for item in data:
            yield make_source_from_dict(item, location)


def find_mk_files(mkpaths: Iterable[Path], ignores: Iterable[str]) -> Iterable[Location]:
    """Find mk files from mk paths, skipping ignores."""

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
