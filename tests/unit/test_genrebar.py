import pytest

from games.domainmodel.model import *
import games.adapters.repository as repo
import games.genre_bases.services as services
from typing import List, Iterable
from games.adapters.repository import AbstractRepository


def test_repo_num_of_search_genre(in_memory_repo):
    genre = Genre("Action")
    in_memory_repo.get_games_by_genre(genre)
    assert in_memory_repo.get_number_of_search_games() == 380

def test_repo_get_max_page_num(in_memory_repo):
    assert services.get_max_page_num(380,30) == 13

def test_repo_generate_page_list(in_memory_repo):
    assert services.generate_page_list(1,13) == [1,2,3,4]

def test_repo_get_current_display(in_memory_repo):
    assert services.get_current_display(380,30,1) == (1,30)

def test_repo_get_genre_list(in_memory_repo):
    assert len(services.get_genre_list(repo.repo_instance)) == 23

def test_repo_get_games(in_memory_repo):
    genre = Genre("Action")
    in_memory_repo.get_games_by_genre(genre)
    assert len(services.get_games(repo.repo_instance,30,1,"")) == 30
