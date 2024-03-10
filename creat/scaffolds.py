from pathlib import Path

from .configs import x_user_config


class Scaffold:
    _root: Path

    def __init__(self, root: Path) -> None:
        self._root = root

    @property
    def root(self) -> Path:
        return self._root

    @property
    def id(self) -> str:
        return self.root.name


def build_index() -> dict[str, Scaffold]:
    scaffolds = {}
    for roots in x_user_config().scaffolds_roots:
        if roots.is_dir():
            for root in roots.iterdir():
                scaffold = Scaffold(root)
                scaffolds[scaffold.id] = scaffold
    return scaffolds
