import json
from pathlib import Path
from typing import Annotated, Optional

import typer

from . import __version__, app
from .configs import GlobalConfig, set_global_config


def _version(value: bool) -> None:
    if value:
        typer.echo(f"creat {__version__}")
        raise typer.Exit(0)


@app.callback()
def main(
    _version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            callback=_version,
            is_eager=True,
        ),
    ] = None,
    global_config_path: Path = typer.Option(
        Path("~/.config/creat/creat.json").expanduser(),
        help="Path to global user config.",
    ),
) -> None:
    """."""
    try:
        with open(global_config_path, "r", encoding="utf-8") as fo:
            data = json.load(fo)
            config_data = GlobalConfig(**data)
    except FileNotFoundError:
        config_data = GlobalConfig()
    set_global_config(config_data)


from . import sample  # noqa
from . import config  # noqa

if __name__ == "__main__":
    app()
