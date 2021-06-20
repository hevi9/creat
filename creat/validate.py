""" Validate correct operation. """

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .ex import ValidateError


def validate(context: Mapping[str, Any]):
    """Validate vars context configuration.

    :raises MkValidateError on validation error.
    """
    target = Path(context["target"])
    if target.exists():
        raise ValidateError(f"{target} already exists")
