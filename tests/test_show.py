""" Test show item flag. """

from creat.find import update_index_from_roots
from creat.index import Index


def test_item_show(mkroot):
    """ Test item show. """
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
    assert source.show is True