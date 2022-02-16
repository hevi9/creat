from __future__ import annotations

from typing import Any, Mapping, Union

from creat.models.actions import Action, Paths


class Move(Action):
    move: Union[str, Paths]

    def run(self, context: Mapping[str, Any]):
        raise NotImplementedError("")
