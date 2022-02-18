# from creat.indexes import Index
# from creat.models.sources import Source
#
#
# class TestIndex:
#     def test_get_empty_to_all(self):
#         index = Index()
#         index.add(Source(tags={"python", "1"}, actions=[]))
#         index.add(Source(tags={"python", "2"}, actions=[]))
#         assert len(list(index.get({}))) == 2
#
#     def test_get_partial(self):
#         index = Index()
#         index.add(Source(tags={"python", "1"}, actions=[]))
#         index.add(Source(tags={"python", "2"}, actions=[]))
#         index.add(Source(tags={"c", "3"}, actions=[]))
#         assert len(list(index.get({"python"}))) == 2
#
#     def test_get_exact_one(self):
#         index = Index()
#         index.add(Source(tags={"python", "1"}, actions=[]))
#         index.add(Source(tags={"python", "2"}, actions=[]))
#         index.add(Source(tags={"c", "3"}, actions=[]))
#         assert len(list(index.get({"python", "2"}))) == 1
