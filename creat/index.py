from __future__ import annotations

from functools import singledispatchmethod
from typing import Dict, Optional
from multidict import MultiDict, MultiMapping

from . import SID_SEP
from .ex import DuplicateSourceError
from .schema import File, Source


class Index:

    _sources: MultiDict[Source]

    def __init__(self):
        self.sources = MultiDict()

    def __repr__(self):
        return f"{self.__class__.__name__}({len(self.sources)})"

    @singledispatchmethod
    def add(self, item) -> Index:
        raise NotImplementedError(
            f"{self.__class__.__name__}.add: not implemented for {type(item)}"
        )

    @add.register
    def _(self, item: File):
        for source in item.sources:
            self.add(source)

    @add.register  # type: ignore
    def _(self, item: Source):
        if self.sources.get(item.sid):
            raise DuplicateSourceError(
                "already exists",
                location=item.location,
                source_id=item.sid,
            )
        self.sources[item.sid] = item

    def find(self, sid: str) -> Source:
        """Find source by name."""
        return self.sources[sid]

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
                return self.find(SID_SEP.join(parts + [use_source_name]))
            except KeyError:
                if not parts:
                    return None
                parts.pop()
                return look(parts)

        source = look(from_source.sid.split(SID_SEP))
        if not source:
            raise KeyError(f"Source {use_source_name} not found")
        return source
