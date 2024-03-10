import os
from pathlib import Path

from rich import print

from rich.rule import Rule


class cd:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._origin = Path().absolute()

    def __enter__(self) -> None:
        print(Rule(title=f"Enter {self._path}", align="left"))
        os.chdir(self._path)

    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        os.chdir(self._origin)
        print(Rule(title=f"Leave {self._path}", align="left"))
