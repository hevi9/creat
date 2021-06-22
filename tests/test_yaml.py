from pathlib import Path

from ruamel.yaml import YAML


def test_load():
    path = Path(__file__).parent / "samples" / "sample01.yaml"
    yaml = YAML()
    data = yaml.load(path)
    for e in data:
        print(e.lc)
