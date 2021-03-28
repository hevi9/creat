""" Test change directory in item ."""

from creat.context import make_root_context
from creat.find import update_index_from_roots
from creat.index import Index
from creat.run import run


def test_item_cd(mkroot, capfd):
    """ Test item cd. """
    root, rel = mkroot.have_dir("target-area")
    target_area = root / rel
    mkroot.have(
        "test/source/action_cd.mk.yaml",
        """
        -   source: action-cd
            make:
            -   mkdir -p ${target}
            -   shell: pwd
                cd: ${target}
        """,
    )
    index = Index()
    update_index_from_roots(index, [mkroot.path_root], [])
    source = index.find("test/source/action-cd")
    context = make_root_context(target_name=str(target_area))
    run(source, context)
    out, _ = capfd.readouterr()
    assert str(target_area) in out
