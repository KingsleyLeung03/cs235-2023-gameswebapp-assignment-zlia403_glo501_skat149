import pytest

from games.domainmodel.model import Game, Genre, Publisher


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

    # Set the new genre, and add it into the repo
    genre = Genre("Visual Novel")
    in_memory_repo.add_genre(genre)

    # Check if the new genre is inside the all genre list
    assert genre in in_memory_repo.get_genre_list()

    # Check if the num of genres has been increased by 1
    assert genre_num + 1 == in_memory_repo.get_number_of_genres()


def test_repo_search_game_by_title(in_memory_repo):
    # Search all games with a title that includes "dragon"
    search_result = in_memory_repo.get_games_by_title_str("dragon")

    # Check if the title of every game from the search result includes "dragon", case-insensitive
    for game in search_result:
        assert "dragon" in game.title.lower()


def test_repo_search_game_by_publisher(in_memory_repo):
    # Set the publisher
    publisher = Publisher("Boogygames Studios")

    # Search all games from the publisher
    search_result = in_memory_repo.get_games_by_publisher(publisher)

    # Check if the num of search results is matched
    assert len(search_result) == 2

    # Check the publisher of every game from the search results
    for game in search_result:
        assert game.publisher == publisher


def test_repo_search_game_by_genre(in_memory_repo):
    # Set the genre
    genre = Genre("Indie")

    # Search all games with this genre
    search_result = in_memory_repo.get_games_by_genre(genre)

    # Check if the num of search results is matched
    assert len(search_result) == 649

    # Check if every game from the search results includes this genre
    for game in search_result:
        assert genre in game.genres


def test_repo_search_game_by_genre_name(in_memory_repo):
    # Set the potential genre, for checking
    genre = Genre("Racing")

    # Search all games with this genre, by name
    search_result = in_memory_repo.get_games_by_genre_str("Racing")

    # Check if the num of search results is matched
    assert len(search_result) == 31

    # Check if every game from the search results includes the potential genre
    for game in search_result:
        assert genre in game.genres
