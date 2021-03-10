# pylint: disable=unused-import

import pytest
from ruamel.yaml.scanner import ScannerError

from mk.find import update_index_from_roots
from mk.index import Index
from mk.location import Location
from mk.run import run
from mk.source_build import make_sources_from_file_yaml
from mk.ui import ui


def test_primary_source(mkroots):
    path_root, path_rel = mkroots["base"]["primary.mk.yaml"]
    for source in make_sources_from_file_yaml(
        Location(path_root=path_root, path_rel=path_rel)
    ):
        assert source.name in ("primary_file", "other_source", "combined")
        assert str(source.location.path_abs).endswith("primary.mk.yaml")
        assert isinstance(source.make, list)


def test_error_1(mkroots):
    path_root, path_rel = mkroots["errors"]["error1.mk.yaml"]
    with pytest.raises(ScannerError) as ex:
        for _ in make_sources_from_file_yaml(
            Location(path_root=path_root, path_rel=path_rel)
        ):
            ...
    msg = str(ex.value)
    assert "error1.mk.yaml" in msg


def test_source_run(mkroot, capfd):
    ui.is_verbose = False
    mkroot.have(
        "sample/.mk.yaml",
        """
        -   source: echo_test
            make:
                - echo testing1
                - echo testing2
                - shell: echo testing3
        """,
    )
    index = Index()
    update_index_from_roots(index, [mkroot.path_root], [])
    source = index.find("sample/echo_test")
    context = {}
    run(source, context)
    out, _ = capfd.readouterr()
    lines = out.split()
    assert lines == ["testing1", "testing2", "testing3"]


def test_source_make_render(mkroot, capfd):
    ui.is_verbose = False
    mkroot.have(
        "test/source/make_render.mk.yaml",
        """
        -   source: super-source
            make:
                -   echo super-source ${target}

                -   use: sub-source-frontend
                    vars:
                        target: ${target}/frontend

                -   use: sub-source-backend
                    vars:
                        target: ${target}/backend

        -   source: sub-source-backend
            make:
                -   echo sub-source-backend ${target}

        -   source: sub-source-frontend
            make:
                -   echo sub-source-frontend ${target}
        """,
    )
    index = Index()
    context = {
        "target": "target-dir",
    }
    update_index_from_roots(index, [mkroot.path_root], [])
    source = index.find("test/source/super-source")
    run(source, context)
    out, _ = capfd.readouterr()
    lines = out.split()
    assert lines == [
        "super-source",
        "target-dir",
        "sub-source-frontend",
        "target-dir/frontend",
        "sub-source-backend",
        "target-dir/backend",
    ]


def test_item_doc_and_show(mkroot):
    ui.is_verbose = False
    mkroot.have(
        "test/source/item_doc_and_show.mk.yaml",
        """
        -   source: source-1
            doc: source-1 doc-1
            show: true
            make:
                -   shell: echo source-1
                    doc: source-1 make shell
                    show: false
        """,
    )
    index = Index()
    update_index_from_roots(index, [mkroot.path_root], [])
    source = index.find("test/source/source-1")
    assert source.doc == "source-1 doc-1"
    assert source.show is True
