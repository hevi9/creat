# pylint: disable=redefined-outer-name

import pytest

from creat.indexes import Index
from creat.models.sources import Source


@pytest.fixture(scope="function")
def index_01():
    index = Index()
    index.add(Source(tags={"python", "1"}, actions=[], cd=None, env=None))
    index.add(Source(tags={"python", "2"}, actions=[], cd=None, env=None))
    index.add(Source(tags={"php", "3"}, actions=[], cd=None, env=None))
    yield index


class TestIndex:
    def test_index_01_sources_count(self, index_01):
        assert len(list(index_01.sources)) == 3

    def test_index_01_get_empty_to_all(self, index_01):
        assert len(list(index_01.get())) == 3

    def test_index_01_get_partial(self, index_01):
        sources = index_01.get({"python"})
        tags = {t for s in sources for t in s.tags}
        assert "1" in tags
        assert "2" in tags
        assert "php" not in tags

    def test_index_01_get_exact_to_one(self, index_01):
        assert len(index_01.get({"python", "1"})) == 1

    def test_index_01_get_error(self, index_01):
        with pytest.raises(KeyError):
            index_01.get({"not exists"})

    def test_index_01_get_tags_count(self, index_01):
        assert len(index_01.get_tags()) == 5

    def test_index_01_get_tags_partial(self, index_01):
        assert index_01.get_tags({"python"}) == {"1", "2"}

    def test_index_01_get_tags_exact_to_empty(self, index_01):
        assert len(index_01.get_tags({"python", "1"})) == 0
