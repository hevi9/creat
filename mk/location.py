""" Source file location. """

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Location:
    """ Source file location. """

    path_root: Path

    path_rel: Path

    def __str__(self) -> str:
        return str(self.path_abs)

    @property
    def path_abs(self) -> Path:
        """ Absolute path to source file. """
        return self.path_root / self.path_rel
