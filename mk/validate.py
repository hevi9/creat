from __future__ import annotations

from pathlib import Path

from .ex import ValidateError


def validate(context: dict):
    target = Path(context["target"])
    if target.exists():
        raise ValidateError(f"{target} already exists")
