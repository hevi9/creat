import sys
from pathlib import Path

import typer
from rich import print

from . import app
from .configs import ScaffoldConfig, json_to_obj, ValidationLocationError
from .configs import get_global_config


@app.command("config-local")
def _config_local(
    init: bool = typer.Option(
        False,
        help="Initialize local config in current directory.",
    ),
    scaffold_path: Path = typer.Argument(
        Path("."),
        help="Path to scaffold root to sample.",
        metavar="PATH",
    ),
) -> None:
    """Print current config of default if node defined."""
    config = get_global_config()
    path = scaffold_path.expanduser() / config.scaffold_config_name
    text = ScaffoldConfig().model_dump_json(indent=2)
    if init:
        if not path.exists():
            print(f"Creating local config file at {path.absolute()}")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
            return
        else:
            print(
                f"[red]Config file {path.absolute()} already exists![/red]. "
                "Remove file if you wan't to "
                "override it."
            )
            raise typer.Exit(1)
    if path.exists():
        try:
            obj = json_to_obj(path, ScaffoldConfig)
            print(obj.model_dump_json(indent=2))
            return
        except ValidationLocationError as ex:
            for error in ex.locations:
                print("ERROR:", error.location, error.msg, f"'{error.subject}'")
            sys.exit(1)
    print(text)
