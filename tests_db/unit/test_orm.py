import pytest

from sqlalchemy.exc import IntegrityError

from games.domainmodel.model import *


def insert_game(empty_session):
    empty_session.execute(
        'INSERT INTO game (id, title, price, release_date, description, image, website, publisher_name) VALUES '
        '(897220, "Summer Pockets", 55.99, "29 Jun, 2018", "From the creators of Angel Beats! and CLANNAD, Key, comes their latest emotional, award-winning journey. Follow protagonist Takahara Hairi as he travels to the secluded island Torishirojima, where he rediscovers what it means to enjoy summer vacation.", "https://cdn.akamai.steamstatic.com/steam/apps/897220/header.jpg?t=1651130440", "http://key.visualarts.gr.jp/summer/", "VisualArts")'
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
    stmt = 'INSERT INTO article_tags (game_id, genre_name) VALUES (:game_id, :genre_name)'
    for genre_key in genre_keys:
        empty_session.execute(stmt, {'article_id': game_key, 'tag_id': genre_key})


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