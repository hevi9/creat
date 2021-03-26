""" Test finding mk files. """

from pathlib import Path

import mk.find


def test_find_mk_files(mkroots):
    """ Test find mk file in roots. """
    for location in mk.find.find_mk_files(
        [mkroots["base"]["."].path_root, mkroots["other"]["."].path_root], [".git"]
    ):
        assert location.path_rel in (
            Path("primary.mk.yaml"),
            Path(".mk.yaml"),
            Path("prj/.mk.yaml"),
        )


def test_find_mk_sources_from_roots(mkroots):
    """ Test find mk file in roots. """
    for source in mk.find.find_mk_sources_from_roots(
        [mkroots["base"]["."].path_root, mkroots["other"]["."].path_root], []
    ):
        assert source.name in ("primary_file", "other_source", "combined")
