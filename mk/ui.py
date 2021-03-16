""" remove """

import sys

import click
from rich.console import Console

console = Console()


class UI:
    """ remove """

    _is_verbose: bool

    def __init__(self, is_verbose: bool = True):
        self._is_verbose = is_verbose

    @property
    def is_verbose(self) -> bool:
        """ remove """
        return self._is_verbose

    @is_verbose.setter
    def is_verbose(self, value: bool):
        self._is_verbose = value

    def error(self, format_text: str, **kwargs):
        """ remove """
        click.secho(
            "Error: " + format_text.format(**kwargs), err=True, bold=True, fg="red"
        )

    def error_exit(self, format_text: str, **kwargs):
        """ remove """
        self.error(format_text, **kwargs)
        sys.exit(1)

    def talk(self, format_text: str, **kwargs):
        """ remove """
        if self.is_verbose:
            click.secho(format_text.format(**kwargs), fg="blue")

    def warn(self, format_text: str, **kwargs):
        """ remove """
        click.secho(format_text.format(**kwargs), fg="orange")

    def create(self, format_text: str, **kwargs):
        """ remove """
        click.secho(format_text.format(**kwargs), fg="green")

    def run(self, format_text: str, **kwargs):
        """ remove """
        if self.is_verbose:
            # click.secho(format_text.format(**kwargs), fg="blue")
            console.rule(format_text.format(**kwargs))


ui = UI()
