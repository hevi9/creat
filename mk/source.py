from __future__ import annotations

import os
from typing import TYPE_CHECKING, Iterable, List, Mapping, Optional

from .location import Location
from .bases import Item, Runnable

if TYPE_CHECKING:
    from .index import Index


class Source(Item, Runnable):

    name: str
    """ Name of the source. """

    make: List[Runnable]
    """ Make list for the source """

    _cd: Optional[str]

    _env: dict

    def __init__(self, name: str, location: Location, control: dict):
        super().__init__(control, location)
        self.name = name
        self.make = []
        self._cd = control.get("cd", None)
        self._env = control.get("env", {})

    def __str__(self):
        return self.id

    @property
    def id(self) -> str:
        return str(self.location.path_rel.parent / self.name).replace("\\", "/")

    @property
    def dir(self) -> str:
        """ Directory where the source is defined. """
        return str(self.location.path_abs.parent)

    def update(self, index: Index) -> None:
        for action in self.make:
            action.update(index)

    def run(self, context: dict) -> None:
        for action in self.make:
            action.run(dict(context, source=self))

    def programs(self) -> Iterable[str]:
        for make in self.make:
            yield from make.programs()

    @property
    def cd(self) -> Optional[str]:
        return self._cd

    @property
    def env(self) -> Mapping[str, str]:
        return dict(os.environ, **self._env)
