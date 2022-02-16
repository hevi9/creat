from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Mapping, Set, Union

from .actions.shell import Shell
from .runnables import Runnable

if TYPE_CHECKING:
    from ..index import Index


class Source(Runnable):
    tags: Set[str]

    actions: List[Union[Shell]]

    def __str__(self):
        return f"{self.__class__.__name__}({self.tags})"

    def __hash__(self):
        return hash("".join(self.tags))

    @property
    def name(self):
        return " ".join(sorted(self.tags))

    @property
    def dir(self) -> str:
        """Directory where the source is defined."""
        return str(self.location.path.parent)

    def run(self, context: Mapping[str, Any]) -> None:
        for action in self.actions:
            action.run(dict(context, source=self))

    def update_index(self, index: Index) -> None:
        for action in self.actions:
            action.update_index(index)
