from __future__ import annotations

from typing import Any, Mapping

from creat.models.actions import Action


class Exe(Action):
    exe: str

    def run(self, context: Mapping[str, Any]):
        raise NotImplementedError("")
