"""Schema for yaml files."""

from __future__ import annotations

from pathlib import Path
from typing import Any, List, Mapping, Optional, Sequence, TypedDict, Union

from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module


class TopLevel(BaseModel):
    sources: List[Any]
    doc: Optional[str]


class Item(BaseModel):
    doc: Optional[str]
    show: bool


class Runnable(Item):
    cd: Optional[str]
    env: Optional[Mapping[str, str]]


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
    with_: Optional[Mapping[str, str]] = Field(alias="with")


class Config(Runnable):
    config: Path
    update: Optional[Any]
    remove: Optional[Any]


class Source(Runnable):
    name: str
    actions: List[Runnable]
