"""Schema for yaml files."""

from __future__ import annotations

from pathlib import Path
from typing import Any, List, Mapping, Optional, Sequence, Union

from pydantic import BaseModel, Field, PrivateAttr  # pylint: disable=no-name-in-module
from typing_extensions import TypedDict

from creat import SID_SEP
from creat.discovers import Location


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
            return {}
        return self.env_

    def run(self, context: Mapping[str, Any]):
        raise NotImplementedError("")


class Action(Runnable):
    def run(self, context: Mapping[str, Any]):
        raise NotImplementedError("")


class Paths(TypedDict):
    src: Path
    dst: Path


class Copy(Action):
    copy_: Union[str, Paths] = Field(alias="copy")

    def run(self, context: Mapping[str, Any]):
        raise NotImplementedError("")


class Move(Action):
    move: Union[str, Paths]

    def run(self, context: Mapping[str, Any]):
        raise NotImplementedError("")


class Remove(Action):
    remove: Union[str, Sequence[Path]]

    def run(self, context: Mapping[str, Any]):
        raise NotImplementedError("")


class Exe(Action):
    exe: str

    def run(self, context: Mapping[str, Any]):
        raise NotImplementedError("")


class Shell(Action):
    shell: str

    def run(self, context: Mapping[str, Any]):
        raise NotImplementedError("")


class Use(Action):
    use: str

    def run(self, context: Mapping[str, Any]):
        raise NotImplementedError("")


class Config(Runnable):
    config: Path
    update: Optional[Any]
    remove: Optional[Any]

    def run(self, context: Mapping[str, Any]):
        raise NotImplementedError("")


class Source(Runnable):
    source: str
    # actions: List[Union[Copy, Move, Remove, Exe, Shell, Use, Config]]
    actions: List[Union[Shell]]

    @property
    def sid(self) -> str:
        if isinstance(self.parent, File):
            return str(self.parent.location.path_rel) + SID_SEP + self.source
        raise TypeError(f"parent {type(self.parent)} not a Location")

    def run(self, context: Mapping[str, Any]):
        raise NotImplementedError("")


class File(Item):
    sources: List[Source]
    _location: Location = PrivateAttr()

    @property
    def location(self) -> Location:
        return self._location

    # class Config:
    #     validate_assignment = False
