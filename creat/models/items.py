from __future__ import annotations

from typing import TYPE_CHECKING, Any, Mapping, Optional

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

from creat.discovers import Location

if TYPE_CHECKING:
    from creat.index import Index


class Item(BaseModel):
    doc: str = ""
    show: bool = True
    parent: Optional[Item] = None
    with_: Optional[Mapping[str, Any]] = Field(alias="with")

    @property
    def location(self) -> Location:
        if not self.parent:
            raise ValueError(f"{self.__class__.__name__}.parent: not set")
        return self.parent.location

    def update_index(self, index: Index) -> None:
        """Update index on pass 2."""
