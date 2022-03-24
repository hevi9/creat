# pylint: disable=no-name-in-module)

from typing import Any, Dict, List, Sequence

from pydantic import BaseModel, ValidationError
from ruamel.yaml import YAML

yaml = YAML(typ="rt")

text = """
top:
    section:
        value1: 1
        value2: foo

    array:
        -   field_int: 1
            field_str: foo
        -   field_int: bar
            field_str: foo
        -   field_int: 3
            field_str: foo

""".strip()


class Section(BaseModel):
    value1: int
    value2: int


class Element(BaseModel):
    field_int: int
    field_str: str


class Top(BaseModel):
    section: Section
    array: List[Element]


class Scope(BaseModel):
    top: Top


def ruamel_yaml_line_number(data: Dict[str, Any], obj_path: Sequence[str]) -> int:
    current = data
    position = None
    for node_name in obj_path:
        # check first sub node
        try:
            # [start_line, col, end_line, col]
            position = current.lc.data[node_name]  # type: ignore
        except AttributeError:  # no .lc
            pass
        except KeyError:  # missing node
            break
        current = current[node_name]
    if position is None:
        raise ValueError(f"Cannot find position for line number from json object path {obj_path}")
    return position[0] + 1


def test_location():
    data = yaml.load(text)
    try:
        _scope = Scope(**data)
    except ValidationError as ex:
        errors = ex.errors()
        for error in errors:
            loc = error["loc"]
            line_number = ruamel_yaml_line_number(data, loc)
            print(line_number, loc, error["msg"])
