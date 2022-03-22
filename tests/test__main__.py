# import click
# import typer
# from typer.testing import CliRunner
#

# noinspection PyProtectedMember


# @pytest.fixture(scope="function")
# def index_01():
#     index = Index()
#     index.add(Source(tags={"basic", "shell"}, actions=[], cd=None, env=None))
#     index.add(Source(tags={"context", "shell"}, actions=[], cd=None, env=None))
#     index.add(Source(tags={"shell", "source"}, actions=[], cd=None, env=None))
#     index.add(Source(tags={"shell", "source", "target"}, actions=[], cd=None, env=None))
#     yield index
#
#
# def test_tags_complete_real(index_01):
#     result = list(_tags_complete_real({"basic"}, "bas", index_01))
#     print(result)


#
# runner = CliRunner()
#
#
# class TestCLI:
#     def test_cli_list(self):
#         r = runner.invoke(
#             app,
#             [
#                 "list",
#             ],
#         )
#         assert not r.exit_code, str(r) + r.stdout
#
#
# def test_source_complete():
#     ctx = typer.Context(command=click.Command("dummy"))
#     choices = list(_source_complete(ctx, "py"))
#     assert choices


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
