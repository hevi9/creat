# from dataclasses import dataclass
# from pathlib import Path
# from typing import Iterable
#
# import pytest
# from pytest_lazyfixture import lazy_fixture
#
# from creat.builds import build_index
#
# cwd = Path(__file__).parent
#
#
# @dataclass
# class Config:
#     roots: Iterable[Path]
#     ignore_globs: Iterable[str]
#
#
# @pytest.fixture(scope="session")
# def config_01():
#     yield Config(
#         roots=[cwd / "samples" / "root01", cwd / "samples" / "root02"],
#         ignore_globs=[".git"],
#     )
#
#
# @pytest.mark.parametrize(
#     "config",
#     [
#         lazy_fixture("config_01"),
#     ],
# )
# class TestBuilds:
#     def test_build(self, config: Config):
#         index = build_index(config.roots, config.ignore_globs)
#         assert index


def test_dummy():
    pass


# @pytest.mark.skipif(True, reason="DEVELOP")
# def test_load():
#     """Test yaml loading"""
#     path = Path(__file__).parent / "samples" / "sample01.yaml"
#     yaml = YAML()
#     data = yaml.load(path)
#     indent = 0
#
#     def traverse(data2):
#         nonlocal indent
#         indent += 1
#         if isinstance(data2, Sequence) and not isinstance(data2, str):
#             print("  " * indent, data2.lc, data2)
#             for e in data2:
#                 traverse(e)
#         elif isinstance(data2, Mapping):
#             print("  " * indent, data2.lc, data2)
#             for _k, v in data2.items():
#                 traverse(v)
#         else:
#             print("  " * indent, data2)
#         indent -= 1
#
#     traverse(data)
#
#
# @pytest.mark.skipif(True, reason="DEVELOP")
# def test_schema():
#     """Test schema validation."""
#     path = Path(__file__).parent / "samples" / "sample01.yaml"
#     yaml = YAML()
#     data = yaml.load(path)
#     data2 = File(sources=data)
#     print(data2, data.lc)
