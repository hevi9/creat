""" Test change directory in item ."""

from mk.context import make_root_context
from mk.find import update_index_from_roots
from mk.index import Index
from mk.run import run
from mk.ui import ui


def test_item_cd(mkroot, capfd):
    """ Test item cd. """
    ui.is_verbose = False
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
    out = out.strip()
    assert out == str(target_area)
