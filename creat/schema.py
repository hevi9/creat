"""Schema for yaml files."""

from __future__ import annotations

from pathlib import Path
from typing import Any, List, Mapping, Sequence, Union

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module
from typing_extensions import TypedDict

from creat.discovers import Location


class Item(BaseModel):
    doc: str | None = None
    show: bool = True
    parent: Item | None = None

    @property
    def location(self) -> Location:
        if not self.parent:
            raise ValueError(f"{self.__class__.__name__}.parent: not set")
        return self.parent.location


class Runnable(Item):
    cd_: str | None = Field(alias="cd")
    env_: Mapping[str, str] | None = Field(alias="env")
    with_: Mapping[str, str] | None = Field(alias="with")

    @property
    def env(self) -> Mapping[str, str]:
        if not self.env_:
            if self.parent and isinstance(self.parent, Runnable):
                return self.parent.env
            return {}
        return self.env_


class Action(Runnable):
    pass


class Paths(TypedDict):
    src: Path
    dst: Path


class Copy(Action):
    copy_: str | Paths = Field(alias="copy")


class Move(Action):
    move: str | Paths


class Remove(Action):
    remove: str | Sequence[Path]


class Exe(Action):
    exe: str


class Shell(Action):
    shell: str


class Use(Action):
    use: str


class Config(Runnable):
    config: Path
    update: Any | None
    remove: Any | None


class Source(Runnable):
    source: str
    actions: List[Union[Copy, Move, Remove, Exe, Shell, Use, Config]]


class File(Item):
    sources: List[Source]
    location_: Location

    @property
    def location(self) -> Location:
        return self.location_
