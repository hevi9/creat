from pathlib import Path

import typer
from rich import print

from ..configs import (
    ScaffoldConfig,
    json_to_obj,
    ValidationLocationError,
    x_user_config,
)

cli = typer.Typer(name="config", no_args_is_help=True, help="Configuration info.")


@cli.command()
def user():
    """User configuration."""
    print(x_user_config().model_dump_json(indent=2))


@cli.command()
def scaffold(
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
    path = scaffold_path.expanduser() / x_user_config().scaffold_config_name
    text = ScaffoldConfig().model_dump_json(indent=2)
    if init:
        if not path.exists():
            print(f"Creating local config file at {path.absolute()}")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
            raise typer.Exit(0)
        else:
            print(
                f"[red]Config file {path.absolute()} already exists![/red]. "
                "Remove file if you want to "
                "override it."
            )
            raise typer.Exit(1)
    if path.exists():
        try:
            obj = json_to_obj(path, ScaffoldConfig)
            print(path)
            print(obj.model_dump_json(indent=2))
            return
        except ValidationLocationError as ex:
            for error in ex.locations:
                print("ERROR:", error.location, error.msg, f"'{error.subject}'")
            raise typer.Exit(0)
    print("Default no file")
    print(text)
