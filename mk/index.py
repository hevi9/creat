""" Index to contain and access sources. """

from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Iterable

from .ex import MkDuplicateSourceError

if TYPE_CHECKING:
    from .source import Source


class Index:
    """ Index to contain and access sources. """

    _sources: Dict[str, Source]

    def __init__(self):
        self._sources = {}

    def add_source(self, source: Source) -> None:
        """ Add source to index. """
        if self._sources.get(source.id):
            raise MkDuplicateSourceError(
                "already exists", id2=source.id, location=source.location
            )
        self._sources[source.id] = source

    @property
    def sources(self) -> Iterable[Source]:
        """ Sources in index. """
        return self._sources.values()

    def find(self, source_id: str) -> Source:
        """ Find source by name. """
        return self._sources[source_id]

    def find_from(self, use_source_name: str, from_source: Source) -> Source:
        """Find source starting from given source.

        Relative lookup.
        """
        try:
            return self.find(use_source_name)
        except KeyError:
            pass

        def look(parts):
            try:
                return self.find("/".join(parts + [use_source_name]))
            except KeyError:
                if not parts:
                    return None
                parts.pop()
                return look(parts)

        source = look(from_source.id.split("/"))
        if not source:
            raise KeyError(f"Source {use_source_name} not found")
        return source
