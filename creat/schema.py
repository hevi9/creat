"""Schema for yaml files."""

from typing import Any, List

from pydantic import BaseModel  # pylint: disable=no-name-in-module


class TopLevel(BaseModel):
    """Top level."""

    sources: List[Any]
