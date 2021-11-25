from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from . import CREAT_GLOB


@dataclass
class Location:

    path_root: Path

    path_rel: Path

    def __str__(self) -> str:
        return str(self.path)

    @property
    def path(self) -> Path:
        """Absolute path to source file."""
        return self.path_root / self.path_rel


# traverse instead Path.glob("**/*") to avoid traversing ignored dirs, eg. .git
def discover(
    roots: Iterable[Path],
    ignore_globs: Iterable[str],
    creat_globs: Iterable[str] = CREAT_GLOB,
) -> Iterable[Location]:
    def traverse(path_rel):
        path_abs = root / path_rel
        if path_abs.is_dir():
            for entry in path_abs.glob("*"):
                if any(entry.match("**/" + g) for g in ignore_globs):
                    continue
                yield from traverse(path_rel / entry.name)
        else:
            if any(path_abs.match("**/" + g) for g in creat_globs):
                yield Location(path_root=root, path_rel=path_rel)

    for root in roots:
        yield from traverse(Path("."))
