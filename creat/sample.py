from pathlib import Path
from subprocess import run

import typer
from copier import Worker

from . import app

from rich import print


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
    worker = Worker(
        src_path=str(scaffold_path),
        dst_path=sample_path,
        overwrite=True,
        skip_answered=True,
    )
    if not sample_path.exists():
        print("new", sample_path, "from", scaffold_path)
        worker.run_copy()
        run(["git", "-C", str(sample_path), "init"])
        run(["git", "-C", str(sample_path), "add", "."])
        run(["git", "-C", str(sample_path), "commit", "-m", "initial"])
    else:
        print("update", sample_path, "from", scaffold_path)
        worker.run_update()
