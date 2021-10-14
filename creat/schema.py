from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import (
    TYPE_CHECKING,
    Any,
    Iterable,
    List,
    Mapping,
    Optional,
    Sequence,
    Union,
)

from pydantic import BaseModel, Field, PrivateAttr  # pylint: disable=no-name-in-module
from typing_extensions import TypedDict

from creat import get_console
from creat.contexts import render
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


class Runnable(Item):
    cd_: Optional[Path] = Field(alias="cd")
    env_: Optional[Mapping[str, str]] = Field(alias="env")

    @property
    def cd(self) -> Path:
        if not self.cd_:
            if self.parent and isinstance(self.parent, Runnable):
                return self.parent.cd
        return Path.cwd()

    @property
    def env(self) -> Mapping[str, str]:
        env = self.env_ or {}
        if self.parent and isinstance(self.parent, Runnable):
            return {**self.parent.env, **env}
        return {**os.environ, **env}

    def run(self, context: Mapping[str, Any]):
        raise NotImplementedError("")

    def programs(self) -> Iterable[str]:
        return []


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
        cmd_text = render(self.shell, context)
        get_console().print(
            f"[magenta]shell:[/magenta] {cmd_text}",
            style="bold on green",
            justify="center",
        )
        # get_console().print(context)
        subprocess.run(  # pylint: disable=subprocess-run-check
            cmd_text,
            shell=True,  # nosec
            cwd=render(str(self.cd), context) if self.cd else None,
            env=self.env,
        ).check_returncode()  # nosec


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

    def __str__(self):
        return f"{self.__class__.__name__}({self.sid})"

    @property
    def name(self) -> str:
        return self.source

    @property
    def dir(self) -> str:
        """Directory where the source is defined."""
        return str(self.location.path.parent)

    @property
    def sid(self) -> str:
        if isinstance(self.parent, File):
            return str(self.parent.location.path_rel.parent / self.source).replace("\\", "/")
        raise TypeError(f"parent {type(self.parent)} not a Location")

    def run(self, context: Mapping[str, Any]) -> None:
        for action in self.actions:
            action.run(dict(context, source=self))

    def update_index(self, index: Index) -> None:
        for action in self.actions:
            action.update_index(index)

    def programs(self) -> Iterable[str]:
        for action in self.actions:
            yield from action.programs()


class File(Item):
    sources: List[Source]
    _location: Location = PrivateAttr()

    @property
    def location(self) -> Location:
        return self._location
