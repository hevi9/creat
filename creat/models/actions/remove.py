from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence, Union

from creat.models.actions import Action


class Remove(Action):
    remove: Union[str, Sequence[Path]]

    def run(self, context: Mapping[str, Any]):
        raise NotImplementedError("")
