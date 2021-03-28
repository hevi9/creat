""" Test removing files or trees. """

from creat.context import make_root_context
from creat.find import update_index_from_roots
from creat.index import Index
from creat.run import run


def test_source_make_remove_tree_render_list(mkroot):
    """ Test tree removal with render var. """
    mkroot.have(
        "test/source/make_remove_tree.mk.yaml",
        """
        -   source: make-remove-tree
            make:
            -   remove:
                - ${target}/tree-to-be-removed
        """,
    )
    mkroot.have("data/target-root/tree-to-be-removed/to-be-removed-1.txt", "DATA")
    remove_root, remove_rel = mkroot.have(
        "data/target-root/tree-to-be-removed/to-be-removed-2.txt", "DATA"
    )
    remove_dir = (remove_root / remove_rel).parent
    index = Index()
    update_index_from_roots(index, [mkroot.path_root], [])
    source = index.find("test/source/make-remove-tree")
    context = make_root_context("target-root")
    assert remove_dir.is_dir()
    with mkroot.cd("data"):
        run(source, context)
    assert not remove_dir.exists()


def test_source_make_remove_file(mkroot):
    """ Test file removal. """
    mkroot.have(
        "test/source/make_remove_file.mk.yaml",
        """
        -   source: make-remove-file
            make:
            -   remove: to-be-removed.txt
        """,
    )
    remove_root, remove_rel = mkroot.have("data/to-be-removed.txt", "DATA")
    remove_file = remove_root / remove_rel
    index = Index()
    update_index_from_roots(index, [mkroot.path_root], [])
    source = index.find("test/source/make-remove-file")
    assert remove_file.is_file()
    with mkroot.cd("data"):
        run(source, {})
    assert not remove_file.exists()


def test_source_make_remove_tree(mkroot):
    """ Test tree removal. """
    mkroot.have(
        "test/source/make_remove_tree.mk.yaml",
        """
        -   source: make-remove-tree
            make:
            -   remove: tree-to-be-removed
        """,
    )
    mkroot.have("data/tree-to-be-removed/to-be-removed-1.txt", "DATA")
    remove_root, remove_rel = mkroot.have("data/tree-to-be-removed/to-be-removed-2.txt", "DATA")
    remove_dir = (remove_root / remove_rel).parent
    index = Index()
    update_index_from_roots(index, [mkroot.path_root], [])
    source = index.find("test/source/make-remove-tree")
    assert remove_dir.is_dir()
    with mkroot.cd("data"):
        run(source, {})
    assert not remove_dir.exists()


def test_source_make_remove_tree_render(mkroot):
    """ Test tree removal with render. """
    mkroot.have(
        "test/source/make_remove_tree.mk.yaml",
        """
        -   source: make-remove-tree
            make:
            -   remove: ${target}/tree-to-be-removed
        """,
    )
    mkroot.have("data/target-root/tree-to-be-removed/to-be-removed-1.txt", "DATA")
    remove_root, remove_rel = mkroot.have(
        "data/target-root/tree-to-be-removed/to-be-removed-2.txt", "DATA"
    )
    remove_dir = (remove_root / remove_rel).parent
    index = Index()
    update_index_from_roots(index, [mkroot.path_root], [])
    source = index.find("test/source/make-remove-tree")
    context = make_root_context("target-root")
    assert remove_dir.is_dir()
    with mkroot.cd("data"):
        run(source, context)
    assert not remove_dir.exists()
