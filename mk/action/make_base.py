import os
from abc import abstractmethod
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Mapping, Optional

from mk.index import Index
from mk.source import Source
from mk.bases import Item, Runnable


class RunCtx(Item, Runnable):
    """ Base implementation for make items. """

    source: Source
    _cd: Optional[str]
    _env: dict

    def __init__(self, source: Source, control: dict):
        super().__init__(control, source.location)
        self.source = source
        self._cd = control.get("cd", None)
        self._env = control.get("env", {})

    @abstractmethod
    def update(self, index: Index) -> None:
        pass

    def programs(self) -> Iterable[str]:
        return []

    @property
    def cd(self) -> Optional[str]:
        if self._cd:
            return self._cd
        if self.source.cd:
            return self.source.cd
        return None

    @property
    def env(self) -> Mapping[str, str]:
        return dict(self.source.env, **self._env)

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
