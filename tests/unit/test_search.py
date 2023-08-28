import pytest

from typing import List, Iterable
from games.domainmodel.model import *
import games.adapters.repository as repo
import games.search.services as services


def test_repo_num_of_search_genre(in_memory_repo):
    services.get_games_by_genre(in_memory_repo,"action")
    assert in_memory_repo.get_number_of_search_games() == 380

def test_repo_num_of_search_pubisher(in_memory_repo):
    services.get_games_by_publisher(in_memory_repo,"Electronic Arts")
    assert in_memory_repo.get_number_of_search_games() == 1

def test_repo_num_of_search_title(in_memory_repo):
    services.get_games_by_title(in_memory_repo,"apex")
    assert in_memory_repo.get_number_of_search_games() == 1

def test_repo_get_max_page_num(in_memory_repo):
    assert services.get_max_page_num(3,30) == 1

def test_repo_generate_page_list(in_memory_repo):
    assert services.generate_page_list(1,13) == [1,2,3,4]

def test_repo_get_current_display(in_memory_repo):
    assert services.get_current_display(380,30,1) == (1,30)

def test_repo_get_genre_list(in_memory_repo):
    assert len(services.get_genre_list(in_memory_repo)) == 24

def test_repo_get_games(in_memory_repo):
    genre = Genre("Action")
    in_memory_repo.get_games_by_genre(genre)
    assert len(services.get_games(in_memory_repo,30,1,"")) == 30