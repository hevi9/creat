import datetime
import subprocess
from pathlib import Path
from subprocess import run

import typer
from copier import Worker
from rich import print
from rich.panel import Panel
from watchfiles import watch

from ..processes import cd
from ..scaffolds import build_index

cli = typer.Typer(pretty_exceptions_enable=False)


@cli.command(no_args_is_help=True)
def sample(
    scaffold_name: str = typer.Argument(
        ...,
        help="Scaffold name to sample.",
        metavar="SCAFFOLD",
    ),
    sample_path: Path = typer.Option(
        "/tmp/creat/sample",
        help="Path to the sample scaffold.",
    ),
) -> None:
    """Make sample instance from scaffold for development."""
    index = build_index()
    scaffold = index[scaffold_name]
    worker = Worker(
        src_path=str(scaffold.root),
        dst_path=sample_path,
        overwrite=True,
        skip_answered=True,
    )

    def update() -> None:
        if not sample_path.exists():
            print("new", sample_path, "from", scaffold.root)
            worker.run_copy()
            run(["git", "-C", str(sample_path), "init"])
            run(["git", "-C", str(sample_path), "add", "."])
            run(["git", "-C", str(sample_path), "commit", "-m", "initial"])
        else:
            print("recopy", sample_path, "from", scaffold.root)
            worker.run_recopy()

        if scaffold.config.sample.runs:
            print(f"Run sample {sample_path} runs:")
            with cd(sample_path):
                for irun in scaffold.config.sample.runs:
                    try:
                        print(f"Run: '{irun.text}'")
                        subprocess.run(irun.text, shell=True, check=True)
                    except subprocess.CalledProcessError as ex:
                        print(Panel(f"{ex!s}", title="ERROR"))

        dt = datetime.datetime.now().astimezone()
        print(f"{dt.strftime('%Y-%m-%d %H:%M:%S')} Sample target {sample_path} updated")

    update()

    print(f"Watching changes from {scaffold.root!s} ..")
    for changes in watch(scaffold.root, debounce=5000):
        print("changes:", changes)
        update()
