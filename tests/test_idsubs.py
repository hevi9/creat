import re

import pprint

text_in = """

class IDTEST01:
IDTEST02
IDTEST03

""".strip()

text_out = """

""".strip()


class IdSubs:
    def __init__(
        self,
        id_re=r"ID([_a-zA-Z][_a-zA-Z0-9]{0,32})",
    ):
        self.id_pattern = re.compile(id_re)

    def on_match(self, match: re.Match) -> str:
        # pprint.pprint(match, match.group())
        pprint.pprint(match.group(1))
        return "XPROJECTX"

    def sub(self, text: str) -> str:
        return re.sub(self.id_pattern, self.on_match, text)


def test_idsubs():
    """"""
    idsubs = IdSubs()
    text = idsubs.sub(text_in)
    pprint.pprint(text)
