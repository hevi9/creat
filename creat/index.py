from __future__ import annotations

from functools import singledispatchmethod
from typing import Dict, Optional, Iterable
from multidict import MultiDict, MultiMapping

from . import SID_SEP
from .exc import DuplicateSourceError
from .schema import File, Source


class Index:

    _sources: MultiDict[Source]

    def __init__(self):
        self._sources = MultiDict()

    def __repr__(self):
        return f"{self.__class__.__name__}({len(self._sources)})"

    @property
    def sources(self) -> MultiMapping[Source]:
        return self._sources

    @singledispatchmethod
    def add(self, item) -> Index:
        raise NotImplementedError(
            f"{self.__class__.__name__}.add: not implemented for {type(item)}"
        )

    @add.register
    def _(self, item: File):
        for source in item.sources:
            self.add(source)
        return self

    @add.register  # type: ignore
    def _(self, item: Source):
        for name in item.source:
            self._sources.add(name, item)
        return self

    def get(self, keys: Iterable[str]) -> Iterable[Source]:
        keys = set(keys)
        results = set()
        if not keys:
            return set(self._sources.values())
        for key in keys:
            for source in self._sources.getall(key):
                if keys.issubset(source.source):
                    results.add(source)
        return results

    # def find(self, sid: str) -> Source:
    #     """Find source by name."""
    #     return self.sources[sid]

    # def find_from(self, use_source_name: str, from_source: Source) -> Source:
    #     """Find source starting from given source.
    #
    #     Relative lookup.
    #     """
    #     try:
    #         return self.find(use_source_name)
    #     except KeyError:
    #         pass
    #
    #     def look(parts):
    #         try:
    #             return self.find(SID_SEP.join(parts + [use_source_name]))
    #         except KeyError:
    #             if not parts:
    #                 return None
    #             parts.pop()
    #             return look(parts)
    #
    #     source = look(from_source.sid.split(SID_SEP))
    #     if not source:
    #         raise KeyError(f"Source {use_source_name} not found")
    #     return source
