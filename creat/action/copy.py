""" Action to copy tree or file. """

import shlex
from pathlib import Path
from shutil import copytree
from typing import Any, Mapping

from creat.action.bases import Action
from creat.context import render
from creat.source import Source


class Copy(Action):
    """ Action to copy tree or file. """

    path_from: str
    path_to: str

    def __init__(self, source: Source, make_item: dict):
        super().__init__(source, make_item)
        params = make_item["copy"]
        if isinstance(params, str):
            self.path_from, self.path_to = shlex.split(params)
        elif isinstance(params, dict):
            self.path_from = params["from"]
            self.path_to = params["to"]
        else:
            raise ValueError(f"Invalid type {type(params)} for field 'copy' in {source._location}")

    def run(self, context: Mapping[str, Any]) -> None:
        path_from = Path(render(self.path_from, context))
        path_to = Path(render(self.path_to, context))
        with self._run_context():
            copytree(
                path_from,
                path_to,
                symlinks=False,
                ignore=None,
                ignore_dangling_symlinks=False,
                dirs_exist_ok=False,
            )
