import pytest

from sqlalchemy.exc import IntegrityError

from games.domainmodel.model import *


def insert_game(empty_session):
    empty_session.execute(
        'INSERT INTO game (id, title, price, release_date, description, image, website, publisher_name) VALUES '
        '(897220, "Summer Pockets", 55.99, "Jun 29, 2018", "From the creators of Angel Beats! and CLANNAD, Key, comes their latest emotional, award-winning journey. Follow protagonist Takahara Hairi as he travels to the secluded island Torishirojima, where he rediscovers what it means to enjoy summer vacation.", "https://cdn.akamai.steamstatic.com/steam/apps/897220/header.jpg?t=1651130440", "http://key.visualarts.gr.jp/summer/", "VisualArts")'
    )
    row = empty_session.execute('SELECT id from game').fetchone()
    return row[0]


def insert_genres(empty_session):
    empty_session.execute(
        'INSERT INTO genre (genre_name) VALUES ("Adventure"), ("Casual")'
    )
    rows = list(empty_session.execute('SELECT genre_name from genre'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_publisher(empty_session):
    empty_session.execute(
        'INSERT INTO publisher (name) VALUES ("VisualArts")'
    )
    row = empty_session.execute('SELECT name from publisher').fetchone()
    return row[0]


def insert_user(empty_session, values=None):
    new_name = "kingsley"
    new_password = "Test1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO user (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from user where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO user (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from user'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_game_genre_associations(empty_session, game_key, genre_keys):
    stmt = 'INSERT INTO game_genre (game_id, genre_name) VALUES (:game_id, :genre_name)'
    for genre_key in genre_keys:
        empty_session.execute(stmt, {'game_id': game_key, 'genre_name': genre_key})


def insert_reviewed_game(empty_session):
    game_key = insert_game(empty_session)
    user_key = insert_user(empty_session)

    empty_session.execute(
        'INSERT INTO review (user_id, game_id, rating, comment) VALUES '
        '(:user_id, :game_id, 5, "Good Game!"),'
        '(:user_id, :game_id, 1, "Bad Game!")',
        {'user_id': user_key, 'game_id': game_key}
    )

    row = empty_session.execute('SELECT id from game').fetchone()
    return row[0]

def insert_favourited_game(empty_session):
    game_key = insert_game(empty_session)
    user_key = insert_user(empty_session)

    empty_session.execute(
        'INSERT INTO favourite_game (user, game) VALUES '
        '(:user_id, :game_id)',
        {'user_id': user_key, 'game_id': game_key}
    )

    row = empty_session.execute('SELECT id from game').fetchone()
    return row[0]


def make_game():
    game = Game(897220, "Summer Pockets")
    game.price = 55.99
    game.release_date = "Jun 29, 2018"
    game.description = "From the creators of Angel Beats! and CLANNAD, Key, comes their latest emotional, award-winning journey. Follow protagonist Takahara Hairi as he travels to the secluded island Torishirojima, where he rediscovers what it means to enjoy summer vacation."
    game.image_url = "https://cdn.akamai.steamstatic.com/steam/apps/897220/header.jpg?t=1651130440"
    game.website_url = "http://key.visualarts.gr.jp/summer/"
    game.publisher = make_publisher()

    return game


def make_genre():
    genre = Genre("Adventure")
    return genre


def make_publisher():
    publisher = Publisher("VisualArts")
    return publisher


def make_user():
    user = User("kingsley", "Test1234")
    return user


def test_loading_of_game(empty_session):
    game_key = insert_game(empty_session)
    expected_game = make_game()
    fetched_game = empty_session.query(Game).one()

    assert expected_game == fetched_game
    assert game_key == fetched_game.game_id


def test_loading_of_game_with_genre(empty_session):
    game_key = insert_game(empty_session)
    genre_keys = insert_genres(empty_session)
    insert_game_genre_associations(empty_session, game_key, genre_keys)

    game = empty_session.query(Game).get(game_key)
    genres = [empty_session.query(Genre).get(genre) for genre in genre_keys]

    for genre in genres:
        assert genre in game.genres


def test_loading_of_reviewed_game(empty_session):
    insert_reviewed_game(empty_session)

    rows = empty_session.query(Game).all()
    game = rows[0]

    for review in game.reviews:
        assert review.game == game


def test_loading_of_favourite_game(empty_session):
    game_id = insert_favourited_game(empty_session)

    rows = empty_session.query(User).all()
    user = rows[0]

    for favourite_game in user.favourite_games:
        assert favourite_game.game_id == game_id


def test_saving_of_review(empty_session):
    game_key = insert_game(empty_session)
    user_key = insert_user(empty_session, ("kingsley", "Test1234"))

    rows = empty_session.query(Game).all()
    game = rows[0]
    user = empty_session.query(User).filter(User._User__username == "kingsley").one()

    # Create a new Review.
    review_comment = "Great game!"
    review_rating = 5
    review = Review(user, game, review_rating, review_comment)
    user.add_review(review)
    game.add_review(review)

    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, game_id, rating, comment FROM review'))

    assert rows == [(user_key, game_key, review_rating, review_comment)]


def test_saving_of_game(empty_session):
    game = make_game()
    empty_session.add(game)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT id, title, price, release_date, description, image, website, publisher_name FROM game'))
    assert rows == [(897220, "Summer Pockets", 55.99, "Jun 29, 2018", "From the creators of Angel Beats! and CLANNAD, Key, comes their latest emotional, award-winning journey. Follow protagonist Takahara Hairi as he travels to the secluded island Torishirojima, where he rediscovers what it means to enjoy summer vacation.", "https://cdn.akamai.steamstatic.com/steam/apps/897220/header.jpg?t=1651130440", "http://key.visualarts.gr.jp/summer/", "VisualArts")]


def test_loading_of_users(empty_session):
    users = list()
    users.append(("kingsley", "Kingsley1111"))
    users.append(("gordon", "Gordon2222"))
    users.append(("shinnosuke", "Shinnosuke3333"))
    insert_users(empty_session, users)

    expected = [
        User("kingsley", "Kingsley1111"),
        User("gordon", "Gordon2222"),
        User("shinnosuke", "Shinnosuke3333")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM user'))
    assert rows == [("kingsley", "Test1234")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("kingsley", "Test5678"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User("kingsley", "Test114514")
        empty_session.add(user)
        empty_session.commit()

