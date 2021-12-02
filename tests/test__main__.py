from typer.testing import CliRunner

from creat.__main__ import app

runner = CliRunner()


class TestCLI:
    def test_cli_list(self):
        r = runner.invoke(
            app,
            [
                "list",
            ],
        )
        assert not r.exit_code, str(r) + r.stdout


#
#
# @pytest.mark.skip(reason="Not ready yet.")
# def test_cli_new(mkroot, tmp_path):
#     """Test new command functionality."""
#     root, _ = mkroot.have(
#         "source.mk.yaml",
#         """
#         """,
#     )
#     r = runner.invoke(
#         app,
#         [
#             "--path",
#             str(root),
#             "new",
#             "test_source",
#             "test_target",
#         ],
#     )
#     assert r.exit_code == 0, r.stdout
#     assert "" in r.stdout
#
#
# # def test_cli_new_direct(mkroot, tmp_path):
# #     """ """
# #
# #     root, _ = mkroot.have(
# #         "source.mk.yaml",
# #         """
# #         source: test_source
# #         """,
# #     )
# #
# #     creat.__main__._paths = [root]
# #     creat.__main__.new("test_source", " ")
#
#
#
#
# def test_cli_develop(mkroot, tmp_path):
#     """Test develop command functionality."""
#     r = runner.invoke(
#         app,
#         [
#             "develop",
#             "test_source",
#         ],
#     )
#     assert r.exit_code == 0, r.stdout
#     # assert "" in r.stdout
