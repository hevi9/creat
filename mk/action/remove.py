""" Remove file or tree action. """

import os
import stat
from pathlib import Path
from shutil import rmtree
from typing import Any, List, Mapping

from mk import get_console
from mk.action.bases import Action
from mk.context import render
from mk.source import Source

_console = get_console()


def _remove_readonly(func, path, _):
    """ Clear the readonly bit and reattempt the removal. """
    os.chmod(path, stat.S_IWRITE)
    func(path)


class Remove(Action):
    """ Remove files or trees. """

    paths: List[str]

    def __init__(self, source: Source, make_item: dict):
        super().__init__(source, make_item)
        params = make_item["remove"]
        if isinstance(params, str):
            self.paths = params.split()
        elif isinstance(params, list):
            self.paths = params
        else:
            raise ValueError(
                f"Invalid type {type(params)} for field 'remove' in {source._location}"
            )

    def run(self, context: Mapping[str, Any]) -> None:
        # eval
        paths = [Path(render(path, context)) for path in self.paths]
        # run
        for path in paths:
            # "safety" guard
            if len(str(path)) < 3:
                raise ValueError(f"don't remove path {path}")
            if not path.exists():
                _console.print(f"{path} does not exists, no op")
                continue
            with self._run_context():
                if path.is_dir():
                    _console.print(f"remove tree {path}")
                    rmtree(path, onerror=_remove_readonly)
                else:
                    _console.print(f"remove file {path}")
                    os.remove(path)
