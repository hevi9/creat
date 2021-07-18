""" Yaml file testing."""


from collections.abc import Mapping, Sequence
from pathlib import Path

import pytest
from ruamel.yaml import YAML

from creat.schema import File


@pytest.mark.skipif(True, reason="DEVELOP")
def test_load():
    """Test yaml loading"""
    path = Path(__file__).parent / "samples" / "sample01.yaml"
    yaml = YAML()
    data = yaml.load(path)
    indent = 0

    def traverse(data2):
        nonlocal indent
        indent += 1
        if isinstance(data2, Sequence) and not isinstance(data2, str):
            print("  " * indent, data2.lc, data2)
            for e in data2:
                traverse(e)
        elif isinstance(data2, Mapping):
            print("  " * indent, data2.lc, data2)
            for _k, v in data2.items():
                traverse(v)
        else:
            print("  " * indent, data2)
        indent -= 1

    traverse(data)


@pytest.mark.skipif(True, reason="DEVELOP")
def test_schema():
    """Test schema validation."""
    path = Path(__file__).parent / "samples" / "sample01.yaml"
    yaml = YAML()
    data = yaml.load(path)
    data2 = File(sources=data)
    print(data2, data.lc)
