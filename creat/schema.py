"""Schema for yaml files."""

from __future__ import annotations

from pathlib import Path
from typing import Any, List, Mapping, Optional, Sequence, Union

from typing_extensions import TypedDict

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module


class Item(BaseModel):
    doc: Optional[str]
    show: bool = True

    _parent: Optional[Item] = None


class Runnable(Item):
    cd: Optional[str]
    env: Optional[Mapping[str, str]]
    with_: Optional[Mapping[str, str]] = Field(alias="with")


class Paths(TypedDict):
    src: Path
    dst: Path


class Copy(Runnable):
    copy_: Union[str, Paths] = Field(alias="copy")


class Move(Runnable):
    move: Union[str, Paths]


class Remove(Runnable):
    remove: Union[str, Sequence[Path]]


class Exe(Runnable):
    exe: str


class Shell(Runnable):
    shell: str


class Use(Runnable):
    use: str


class Config(Runnable):
    config: Path
    update: Optional[Any]
    remove: Optional[Any]


class Source(Runnable):
    source: str
    actions: List[Union[Copy, Move, Remove, Exe, Shell, Use, Config]]


class TopLevel(Item):
    sources: List[Source]
