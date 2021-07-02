"""Schema for yaml files."""

from __future__ import annotations

from pathlib import Path
from typing import Any, List, Optional, Mapping, TypedDict, Union, Sequence

from pydantic import Field
from pydantic.main import BaseModel


class TopLevel(BaseModel):
    sources: List[Any]


class Item(BaseModel):
    doc: Optional[str]
    show: bool


class Runnable(Item):
    cd: Optional[str]
    env: Optional[Mapping[str, str]]


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


class Source(Runnable):
    name: str
    actions: List[Action]
