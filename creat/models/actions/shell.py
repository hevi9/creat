from __future__ import annotations

import subprocess
from typing import Any, Mapping

from creat import get_console
from creat.contexts import render
from creat.models.actions import Action


class Shell(Action):
    shell: str

    def run(self, context: Mapping[str, Any]):
        cmd_text = render(self.shell, context)
        get_console().print(
            f"[magenta]shell:[/magenta] {cmd_text}",
            style="bold on green",
            justify="center",
        )
        # get_console().print(context)
        subprocess.run(  # pylint: disable=subprocess-run-check
            cmd_text,
            shell=True,  # nosec
            cwd=render(str(self.cd), context) if self.cd else None,
            env=self.env,
        ).check_returncode()  # nosec
