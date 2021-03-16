""" Test use action. """

from mk.find import update_index_from_roots
from mk.index import Index
from mk.run import run
from mk.ui import ui


def test_source_make_use(mkroot, capfd):
    """ Test source to use source. """
    ui.is_verbose = False
    mkroot.have(
        "test/source/make_use.mk.yaml",
        """
        -   source: super-source
            make:
                - use: sub-source-1
                - use: sub-source-2
                - echo super-source
        -   source: sub-source-1
            make:
                - echo sub-source-1
        -   source: sub-source-2
            make:
                - echo sub-source-2
        """,
    )
    index = Index()
    update_index_from_roots(index, [mkroot.path_root], [])
    source = index.find("test/source/super-source")
    context = {}
    run(source, context)
    out, _ = capfd.readouterr()
    lines = out.split()
    assert lines == ["sub-source-1", "sub-source-2", "super-source"]
