import pytest

from games.domainmodel.model import Game, Genre


def test_repo_can_add_a_game(in_memory_repo):
    game = Game(897220, 'Summer Pockets')
    in_memory_repo.add_game(game)

    assert in_memory_repo.get_game_by_id(897220) is game

def test_repo_can_retrieve_a_game(in_memory_repo):
    game = in_memory_repo.get_game_by_id(1002510)

    assert game == Game(1002510, "The Spell - A Kinetic Novel")

def test_repo_retrieves_correct_num_of_game(in_memory_repo):
    game_num = in_memory_repo.get_number_of_games()

    assert game_num == 877

def test_repo_num_of_unique_genre(in_memory_repo):
    genre_num = in_memory_repo.get_number_of_genres()

    assert genre_num == 24

def test_repo_add_new_genre_and_increase_count(in_memory_repo):
    # Get the origin num of genres
    genre_num = in_memory_repo.get_number_of_genres()

    genre = Genre("Visual Novel")
    in_memory_repo.add_genre(genre)

    # Check if the new genre is inside the all genre list
    assert genre in in_memory_repo.get_genre_list()

    # Check if the num of genres has been increased by 1
    assert genre_num + 1 == in_memory_repo.get_number_of_genres()

