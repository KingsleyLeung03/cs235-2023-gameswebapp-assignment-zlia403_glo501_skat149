import pytest

from games import create_app
from games.adapters import memory_repository
from games.adapters.memory_repository import MemoryRepository
from pathlib import Path

TEST_DATA_PATH = Path('games') / 'adapters' / 'data'

@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH, repo)
    return repo


@pytest.fixture
def client():
    my_app = create_app()

    return my_app.test_client()
