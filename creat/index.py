""" Index to contain and access sources. """

from __future__ import annotations

from functools import singledispatchmethod
from typing import Dict, Iterable, ForwardRef

from .ex import DuplicateSourceError
from .schema import File, Source


Index = ForwardRef("Index")


class Index:
    """Index to contain and access sources."""

    _sources: Dict[str, Source]

    def __init__(self):
        self._sources = {}

    @singledispatchmethod
    def add(self, item) -> Index:
        raise NotImplementedError(
            f"{self.__class__.__name__}.add: not implemented for {type(item)}"
        )

    @add.register
    def _(self, item: File) -> Index:
        for source in item.sources:
            self.add(source)
        return self

    @add.register
    def _(self, item: Source) -> Index:
        if self._sources.get(item.id):
            raise DuplicateSourceError(
                "already exists",
                id2=item.id,
                location=item.location,
            )
        self._sources[item.id] = item
        return self

    @property
    def sources(self) -> Iterable[Source]:
        """Sources in index."""
        return self._sources.values()

    def find(self, source_id: str) -> Source:
        """Find source by name."""
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

    __instance: Index = None

    @classmethod
    def get(cls) -> Index:
        if not cls.__instance:
            cls.__instance = Index()
        return cls.__instance
