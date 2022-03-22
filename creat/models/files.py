from __future__ import annotations

from typing import List

from pydantic import PrivateAttr

from creat.discovers import Location
from creat.models.items import Item
from creat.models.sources import Source


class File(Item):
    sources: List[Source]
    _location: Location = PrivateAttr()

    def post_init(self, location: Location):
        self._location = location

    @property
    def location(self) -> Location:
        return self._location
