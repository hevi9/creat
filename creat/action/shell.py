""" Shell execution action. """

import subprocess  # nosec
from typing import Any, Mapping

from creat import get_console
from creat.action.bases import Action
from creat.context import render
from creat.source import Source

_console = get_console()


class Shell(Action):
    """ Shell execution action. """

    def __init__(self, source: Source, make_item: dict):
        super().__init__(source, make_item)
        self.cmd_text = make_item["shell"]

    def run(self, context: Mapping[str, Any]):
        cmd_text = render(self.cmd_text, context)
        _console.print(f"{cmd_text}")
        subprocess.run(  # pylint: disable=subprocess-run-check
            cmd_text,
            shell=True,  # nosec
            cwd=render(self.cd, context) if self.cd else None,
            env=self.env,
        ).check_returncode()  # nosec

    def programs(self):
        # TODO: implement programs
        # parts = shlex.split(self.cmd_text)
        ...
