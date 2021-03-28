""" Test cli functionality. """
import pytest
from typer.testing import CliRunner

from creat.__main__ import app

runner = CliRunner()


@pytest.mark.skip(reason="Not ready yet.")
def test_cli_new(mkroot, tmp_path):
    """ Test new command functionality. """
    root, _ = mkroot.have(
        "source.mk.yaml",
        """
        """,
    )
    r = runner.invoke(
        app,
        [
            "--path",
            str(root),
            "new",
            "test_source",
            "test_target",
        ],
    )
    assert r.exit_code == 0, r.stdout
    # assert "" in r.stdout


def test_cli_list(mkroot):
    """ Test list command functionality. """
    r = runner.invoke(
        app,
        [
            "list",
        ],
    )
    assert r.exit_code == 0, r.stdout
    # assert "" in r.stdout


def test_cli_develop(mkroot, tmp_path):
    """ Test develop command functionality. """
    r = runner.invoke(
        app,
        [
            "develop",
            "test_source",
        ],
    )
    assert r.exit_code == 0, r.stdout
    # assert "" in r.stdout
