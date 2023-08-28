import pytest

from games.domainmodel.model import Game


def test_repo_can_add_a_game(in_memory_repo):
    game_num_og = in_memory_repo.get_number_of_games()

    game = Game(897220, 'Summer Pockets')
    in_memory_repo.add_game(game)

    assert in_memory_repo.get_game_by_id(897220) is game

def test_repo_can_retrieve_a_game(in_memory_repo):
    game = in_memory_repo.get_game_by_id(1002510)

    assert game == Game(1002510, "The Spell - A Kinetic Novel")
