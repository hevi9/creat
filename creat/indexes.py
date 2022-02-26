from __future__ import annotations

from functools import singledispatchmethod
from typing import Collection, Optional, Set

from loguru import logger
from multidict import MultiDict, MutableMultiMapping

from .models.files import File
from .models.sources import Source


class Index:

    _tag_to_sources: MutableMultiMapping[Source]

    def __init__(self):
        self._tag_to_sources = MultiDict()

    def __repr__(self):
        return f"{self.__class__.__name__}({len(self._tag_to_sources)})"

    @property
    def sources(self) -> Collection[Source]:
        return set(self._tag_to_sources.values())

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
            self._tag_to_sources.add(name, item)
        return self

    def get(self, tags: Optional[Set[str]] = None) -> Collection[Source]:
        """Get sources based in index.tags set difference tags.

        Args:
            tags: Tags to define difference. Empty set or None results all
            sources in index. Non-existent tags raises KeyError. All matching
            tags results one source.
        """
        if not tags:
            return set(self._tag_to_sources.values())
        results = set()
        for tag in tags:
            for source in self._tag_to_sources.getall(tag):
                if tags.issubset(source.tags):
                    results.add(source)
        return results

    def get_tags(self, tags: Optional[Set[str]] = None) -> Collection[str]:
        """Get index.tags set difference tags.

        Args:
            tags: Tags to define difference. Empty set or None results all
            tags in index. Non-existent tags raises KeyError. All matching
            tags results empty collection.
        """
        if not tags:
            return set(self._tag_to_sources.keys())
        results = set()
        for tag in tags:
            for source in self._tag_to_sources.getall(tag):
                if tags.issubset(source.tags):
                    results.update(source.tags - tags)
        return results
