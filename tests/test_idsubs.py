import re
from pathlib import Path
from typing import Mapping

from loguru import logger

import pytest

import charset_normalizer

text_in = """

class IDTEST01:
IDTEST02
IDTEST03
IDx

""".strip()

text_out = """
class REPLACED01:\nREPLACED02\nREPLACED03\nREPLACEDx
""".strip()

text_substitutions = {
    "TEST01": "REPLACED01",
    "TEST02": "REPLACED02",
    "TEST03": "REPLACED03",
    "x": "REPLACEDx",
}


class IdSubs:
    def __init__(
        self,
        substitutions: Mapping[str, str],
        id_re: str = r"ID([_a-zA-Z][_a-zA-Z0-9]*)",
    ):
        self.id_pattern = re.compile(id_re)
        self.substitutions = substitutions
        self.log = logger.bind(
            substitutions=substitutions,
            id_re=id_re,
        )

    def on_match(self, match: re.Match) -> str:
        source = match.group(1)
        try:
            target = self.substitutions[source]
            self.log.debug(f"source={source} target={target}")
            return target
        except KeyError:
            raise KeyError(f"`{source}` not found in substitutions")

    def sub(self, text: str) -> str:
        return re.sub(self.id_pattern, self.on_match, text)

    def sub_file(self, file_in: Path, file_out: Path | None = None) -> None:
        if charset_normalizer.is_binary(file_in):
            raise ValueError(f"File {file_in} is binary")
        file_out = file_out or file_in
        if not file_out.parent.is_dir():
            raise FileNotFoundError(f"Directory {file_out.parent} not exists")
        text = file_in.read_text()
        text_sub = self.sub(text)
        file_out.write_text(text_sub)

    def sub_path(self, path: Path) -> None:
        raise NotImplementedError

    def sub_tree(self, path: Path) -> None:
        raise NotImplementedError


@pytest.fixture(scope="function")
def files(tmp_path: Path):
    paths = (
        tmp_path / "text_in.txt",
        tmp_path / "text_out.txt",
        tmp_path / "text_result.txt",
    )
    paths[0].write_text(text_in)
    paths[1].write_text(text_out)
    yield paths


def test_idsubs():
    idsubs = IdSubs(substitutions=text_substitutions)
    text_result = idsubs.sub(text_in)
    assert text_result == text_out


def test_idsubs_from_files(files):
    idsubs = IdSubs(substitutions=text_substitutions)
    idsubs.sub_file(file_in=files[0], file_out=files[2])
    assert files[1].read_text() == files[2].read_text()
