from collections.abc import Iterator

import pytest

from creat.configs.config import config_slot


@pytest.fixture(autouse=True)
def _reset_config_slot() -> Iterator[None]:
    """Ensure each test starts with a clean config slot."""
    yield
    config_slot.reset()
