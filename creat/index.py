from __future__ import annotations

from functools import singledispatchmethod
from typing import Iterable, Set

from loguru import logger
from multidict import MultiDict

from .models.files import File
from .models.sources import Source


class Index:

    _sources: MultiDict[Source]

    def __init__(self):
        self._sources = MultiDict()

    def __repr__(self):
        return f"{self.__class__.__name__}({len(self._sources)})"

    @property
    def sources(self) -> Set[Source]:
        # sources exists multiple times per tag -> source mapping
        return set(self._sources.values())

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
        logger.debug("Index.add(): add source {}", item)
        for name in item.tags:
            logger.debug("Index.add(): add name:source", item, name=name, tags=str(item))
            self._sources.add(name, item)
        return self

    def get(self, keys: Iterable[str]) -> Iterable[Source]:
        keys = set(keys)
        results = set()
        if not keys:
            return set(self._sources.values())
        for key in keys:
            for source in self._sources.getall(key):
                if keys.issubset(source.tags):
                    results.add(source)
        return results
