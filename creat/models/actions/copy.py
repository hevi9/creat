from __future__ import annotations

from typing import Any, Mapping, Union

from pydantic import Field

from creat.models.actions import Action, Paths


class Copy(Action):
    copy_: Union[str, Paths] = Field(alias="copy")

    def run(self, context: Mapping[str, Any]):
        raise NotImplementedError("")
