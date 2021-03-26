""" Test move operation. """

import pytest


@pytest.mark.skip(reason="TODO")
def test_source_make_move(mkroot):
    """ Test move tree. """
    mkroot.have(
        "test/source/make_cmd.mk.yaml",
        """
        -   source: cmd-source
            make:
            -   cmd: copy source-file target-file
            -   cmd: copy source-tree target-tree
            -   cmd: move source-tree target-tree
            -   cmd: remove remove-tree-1
        -   source: cmd-source-2
            make:
            -   copy: source-file target-file
            -   copy: source-tree target-tree
            -   move: source-tree target-tree
            -   remove: remove-tree-1
        """,
    )
