""" Test copy operation. """

import pytest

from mk.context import make_root_context
from mk.find import update_index_from_roots
from mk.index import Index
from mk.run import run
from mk.ui import ui


@pytest.mark.skip(reason="TODO")
def test_source_make_copy_file(mkroot):
    """ Test copy a file. """
    ui.is_verbose = False
    mkroot.have(
        "test/source/make_copy.mk.yaml",
        """
        -   source: cmd-source
            make:
            -   cmd: copy source-file target-file
            -   cmd: copy source-tree target-tree
            -   cmd: move source-tree target-tree
            -   cmd: remove remove-tree-1
        """,
    )


def test_source_make_copy_tree(mkroot):
    """ Test copy a tree. """
    ui.is_verbose = False
    mkroot.have(
        "test/source/make_copy_tree.mk.yaml",
        """
        -   source: make-copy-tree
            make:
            -   copy: ${source.dir}/source-tree target-tree-1
            -   copy:
                    from: ${source.dir}/source-tree
                    to: target-tree-2
        """,
    )
    mkroot.have("test/source/source-tree/.gitignore", "DATA")
    mkroot.have("test/source/source-tree/README.md", "DATA")
    root_path, target_rel = mkroot.have_dir("test/target-area")
    target_area = root_path / target_rel
    #
    index = Index()
    update_index_from_roots(index, [mkroot.path_root], [])
    source = index.find("test/source/make-copy-tree")
    context = make_root_context("target-root")
    with mkroot.cd(target_area):
        run(source, context)
    assert (target_area / "target-tree-1" / ".gitignore").exists()
    assert (target_area / "target-tree-2" / ".gitignore").exists()
