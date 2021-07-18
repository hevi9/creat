""" Test copy operation. """
from pathlib import Path

import pytest

from creat.builds import update_index_from_roots, load
from creat.contexts import make_root_context
from creat.index import Index
from creat.location import Location
from creat.run import run
from creat.schema import File

from rich import print


@pytest.mark.skipif(False, reason="TODO")
def test_copy_file():
    """Test copy a file."""

    location = Location(
        path_root=Path(__file__).parent / "samples",
        path_rel=Path("copy.creat.yaml"),
    )
    data1 = load(location)
    data2 = File(**data1, location_=location)

    print(data2)

    # mkroot.have(
    #     "test/source/make_copy.mk.yaml",
    #     """
    #     -   source: cmd-source
    #         make:
    #         -   cmd: copy source-file target-file
    #         -   cmd: copy source-tree target-tree
    #         -   cmd: move source-tree target-tree
    #         -   cmd: remove remove-tree-1
    #     """,
    # )

    # create_roots = None
    # ignores = None
    # context = make_context(target="target")
    # index = build(roots=create_roots, ignores=ignores)
    # source = index.find(source="test-copy-file")
    # source.run(context)


def test_copy_tree(mkroot):
    """Test copy a tree."""
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
