import os
from abc import abstractmethod
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Mapping, Optional

from mk.bases import Item, Runnable
from mk.index import Index
from mk.source import Source


class RunCtx(Item, Runnable):
    """ Base implementation for make items. """

    _source: Source
    _cd: Optional[str]
    _env: dict

    def __init__(self, source: Source, control: dict):
        super().__init__(control, source._location)
        self._source = source
        self._cd = control.get("cd", None)
        self._env = control.get("env", {})

    @property
    def cd(self) -> Optional[str]:
        if self._cd:
            return self._cd
        if self._source.cd:
            return self._source.cd
        return None

    @property
    def env(self) -> Mapping[str, str]:
        return dict(self._source.env, **self._env)

    def update(self, index: Index) -> None:
        pass  # not all runnable need to update

    def programs(self) -> Iterable[str]:
        return []

    @contextmanager
    def _run_context(self):
        if self.cd:
            cwd_old = Path.cwd()
            try:
                os.chdir(self.cd)
                yield self.cd, self.env
            finally:
                os.chdir(cwd_old)
        else:
            yield None, self.env

    @abstractmethod
    def run(self, context: dict) -> None:
        pass
