import json
import sys
from pathlib import Path

import typer
from json_source_map import calculate  # type: ignore
from pydantic_core import ValidationError
from rich import print

from . import app
from .configs import LocalConfig
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
    path = scaffold_path.expanduser() / config.local_config_name
    text = LocalConfig().model_dump_json(indent=2)
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
            with open(path, "r", encoding="utf-8") as fo:
                data = json.load(fo)
                local_config = LocalConfig(**data)
                print(local_config.model_dump_json(indent=2))
            return
        except ValidationError as ex:
            with open(path, "r", encoding="utf-8") as fo:
                text = fo.read()
            source_map = calculate(text)
            for error in ex.errors():
                # todo implement dict up tracking when exact pointer is not found
                location_path = list(error["loc"])
                error_context_path = None
                while location_path:
                    try:
                        pointer = "/" + "/".join([str(i) for i in location_path])
                        error_context_path = source_map[pointer]
                        break
                    except KeyError:
                        location_path.pop()
                        continue
                if error_context_path is not None:
                    line = error_context_path.value_end.line
                    column = error_context_path.value_end.column
                    location = f"{path!s}:{line}:{column}"
                    subject = error["loc"][-1]
                    print(location, error["msg"], subject)
                else:
                    print(error)
            sys.exit(1)
    print(text)
