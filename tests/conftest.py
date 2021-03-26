""" Fixture for mk tests. """

# pylint: disable=redefined-outer-name

import os
from contextlib import contextmanager
from pathlib import Path
from textwrap import dedent
from typing import Dict, Tuple, Union

import pytest

SOURCE_PRIMARY = """
- source: primary_file
  make:
    - echo primary_file
- source: other_source
  make:
    - echo other source
- source: combined
  make:
    - primary_file
    - other_source

""".strip()

SOURCE_ERROR_1 = """
- FI
- SE
NO
""".strip()

SOURCE_ERROR_2 = """
- FI
al dkaswdkas - SE
- NO
""".strip()


class Root:
    """ Root fixture directory to create testing files and directories.  """

    def __init__(self, path_root: Path):
        self.path_root = path_root

    @property
    def path_abs(self):
        """ Absolute path """
        return self.path_root.resolve()

    @contextmanager
    def cd(self, path: Union[Path, str]):
        """ with context to cd into directory. """
        path = Path(path)
        cwd_old = Path.cwd()
        if not path.is_absolute():
            path = self.path_root / path
        try:
            os.chdir(path)
            yield path
        finally:
            os.chdir(cwd_old)

    def have(self, path_rel: Union[Path, str], text: str) -> Tuple[Path, Path]:
        """ Have a file under root with text content. """
        path_rel = Path(path_rel)
        path_abs = self.path_root / path_rel
        path_abs.parent.mkdir(parents=True, exist_ok=True)
        text = dedent(text)
        with open(path_abs, "w") as fo:
            fo.write(text)
        return self.path_root, path_rel

    def have_dir(self, path_rel: Union[Path, str]) -> Tuple[Path, Path]:
        """Have a directory under root."""
        path_rel = Path(path_rel)
        path_abs = self.path_root / path_rel
        path_abs.mkdir(parents=True, exist_ok=True)
        return self.path_root, path_rel


@pytest.fixture(scope="function")
def mkroot(tmp_path_factory) -> Root:
    """ Get a temporary mk root. """
    return Root(tmp_path_factory.mktemp("root"))


@pytest.fixture(scope="session")
def mkroots(tmp_path_factory) -> Dict:
    """ Get a temporary premade mkroot structure. """
    root_base = Root(tmp_path_factory.mktemp("base"))
    root_other = Root(tmp_path_factory.mktemp("other"))
    root_errors = Root(tmp_path_factory.mktemp("errors"))
    return {
        "base": {
            ".": root_base,
            "primary.mk.yaml": root_base.have("primary.mk.yaml", SOURCE_PRIMARY),
            ".mk.yaml": root_base.have(".mk.yaml", SOURCE_PRIMARY),
            "prj": {
                ".mk.yaml": root_base.have("prj/.mk.yaml", SOURCE_PRIMARY),
            },
        },
        "other": {".": root_other},
        "errors": {
            ".": root_errors,
            "error1.mk.yaml": root_errors.have("error1.mk.yaml", SOURCE_ERROR_1),
            "error2.mk.yaml": root_errors.have("error2.mk.yaml", SOURCE_ERROR_2),
        },
    }


@pytest.fixture(scope="session")
def mkprimary(mkroots) -> Tuple[Path, Path]:
    """ Primary mk file. """
    return mkroots["base"]["primary.mk.yaml"]


@pytest.fixture(scope="session")
def mkerror(mkroots) -> Tuple[Path, Path]:
    """ Errorful mk file. """
    return mkroots["errors"]["error1.mk.yaml"]
