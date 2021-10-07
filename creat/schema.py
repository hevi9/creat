"""Schema for yaml files."""

from __future__ import annotations

from pathlib import Path
from typing import Any, List, Mapping, Optional, Sequence, Union

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module
from typing_extensions import TypedDict

from creat.location import Location


class Item(BaseModel):
    doc: Optional[str] = None
    show: bool = True
    parent: Optional[Item] = None

    @property
    def location(self) -> Location:
        if not self.parent:
            raise ValueError(f"{self.__class__.__name__}.parent: not set")
        return self.parent.location


class Runnable(Item):
    cd_: Optional[str] = Field(alias="cd")
    env_: Optional[Mapping[str, str]] = Field(alias="env")
    with_: Optional[Mapping[str, str]] = Field(alias="with")

    @property
    def env(self) -> Mapping[str, str]:
        if not self.env_:
            if self.parent and isinstance(self.parent, Runnable):
                return self.parent.env
            else:
                return {}
        return self.env_


class Action(Runnable):
    pass


class Paths(TypedDict):
    src: Path
    dst: Path


class Copy(Action):
    copy_: Union[str, Paths] = Field(alias="copy")


class Move(Action):
    move: Union[str, Paths]


class Remove(Action):
    remove: Union[str, Sequence[Path]]


class Exe(Action):
    exe: str


class Shell(Action):
    shell: str


class Use(Action):
    use: str


class Config(Runnable):
    config: Path
    update: Optional[Any]
    remove: Optional[Any]


class Source(Runnable):
    source: str
    actions: List[Union[Copy, Move, Remove, Exe, Shell, Use, Config]]


class File(Item):
    sources: List[Source]
    location_: Location

    @property
    def location(self) -> Location:
        return self.location_
