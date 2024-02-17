from pathlib import Path
from typing import Annotated, Optional

import typer

from . import __version__, app
from .configs import UserConfig, init_user_config, x_user_config, json_to_obj


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
    user_config_path: Path = typer.Option(
        Path("~/.config/creat/creat.json").expanduser(),
        help="Path to user config.",
    ),
) -> None:
    """."""
    try:
        config_data = json_to_obj(user_config_path, UserConfig)
    except FileNotFoundError:
        config_data = UserConfig()
    config_data.user_config_path = user_config_path
    x_user_config.init(config_data)

    init_user_config(config_data)


from . import sample  # noqa
from . import config  # noqa

if __name__ == "__main__":
    app()
