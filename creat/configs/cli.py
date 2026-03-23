from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

import typer

from creat.configs import ConfigValidationError


@contextmanager
def config_validation_cli_handler() -> Iterator[None]:
    """Render config validation failures as Typer-friendly CLI errors."""
    try:
        yield
    except ConfigValidationError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc
