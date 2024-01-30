from typing import Annotated, Optional

import typer

from . import __version__, app


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
) -> None:
    """."""


from . import sample  # noqa

if __name__ == "__main__":
    app()
