from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from typing_extensions import TypedDict

from creat.models.runnables import Runnable


class Action(Runnable):
    def run(self, context: Mapping[str, Any]):
        raise NotImplementedError("")


class Paths(TypedDict):
    src: Path
    dst: Path
