import pytest

from games import create_app
from games.adapters import memory_repository
from games.adapters.memory_repository import MemoryRepository


@pytest.fixture
def in_memory_repo():
    repo = MemoryRepository()
    memory_repository.populate(repo)
    return repo


@pytest.fixture
def client():
    my_app = create_app()

    return my_app.test_client()
