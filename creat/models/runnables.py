from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Iterable, Mapping, Optional

from pydantic import Field

from creat.models.items import Item


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
