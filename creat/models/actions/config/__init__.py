from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Optional

from creat.models.runnables import Runnable


class ConfigFile(Runnable):
    config: Path
    update: Optional[Any]
    remove: Optional[Any]

    def run(self, context: Mapping[str, Any]):
        raise NotImplementedError("")
