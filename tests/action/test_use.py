""" Test use action. """

from creat.find import update_index_from_roots
from creat.index import Index
from creat.run import run


def test_source_make_use(mkroot, capfd):
    """ Test source to use source. """
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
    for check in ["sub-source-1", "sub-source-2", "super-source"]:
        assert check in out
