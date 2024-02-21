from pathlib import Path
from subprocess import run

import typer
from copier import Worker

from . import app

from rich import print

from watchfiles import watch

import datetime


@app.command("sample")
def _sample(
    scaffold_path: Path = typer.Argument(
        ...,
        help="Path to scaffold root to sample.",
        metavar="PATH",
    ),
) -> None:
    """Make sample instance from scaffold for development."""
    sample_path = Path("/tmp/creat/sample")
    scaffold_path = scaffold_path.expanduser()
    worker = Worker(
        src_path=str(scaffold_path),
        dst_path=sample_path,
        overwrite=True,
        skip_answered=True,
    )

    def update() -> None:
        if not sample_path.exists():
            print("new", sample_path, "from", scaffold_path)
            worker.run_copy()
            run(["git", "-C", str(sample_path), "init"])
            run(["git", "-C", str(sample_path), "add", "."])
            run(["git", "-C", str(sample_path), "commit", "-m", "initial"])
        else:
            print("recopy", sample_path, "from", scaffold_path)
            worker.run_recopy()
        dt = datetime.datetime.now()
        print(f"{dt.strftime('%Y%m%dT%H%M%S')} {sample_path} updated")

    update()

    print(f"Watching changes from {scaffold_path!s} ..")
    for changes in watch(scaffold_path, debounce=5000):
        print(changes)
        update()
