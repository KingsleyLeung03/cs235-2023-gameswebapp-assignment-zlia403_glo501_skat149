import pytest

from flask import session

# Test registering




# Test logging in




# Test browsing games
def test_e2e_layout_page(client):
    # Check that we can retrieve the layout page.
    response = client.get('/')
    response_layout = client.get('/layout')
    assert response.status_code == 200
    assert response_layout.status_code == 200

    # Check that the introduction is included on the page.
    assert b'Welcome to the CS235 Game Library!' in response.data
    assert b'Welcome to the CS235 Game Library!' in response_layout.data

def test_e2e_games_page_default(client):
    # Check that we can retrieve the games page.
    response = client.get('/games')
    assert response.status_code == 200

    # Check that the first 3 games we need are included on the page.
    assert b'Xpand Rally' in response.data
    assert b'Call of Duty' in response.data
    assert b'Nikopol: Secrets of the Immortals' in response.data

def test_e2e_games_page_with_page_num(client):
    # Check that we can retrieve the games page with page num.
    response_page_1 = client.get('/games?page=1')
    response_page_2 = client.get('/games?page=2')
    assert response_page_1.status_code == 200
    assert response_page_2.status_code == 200

    # Check that the first 3 games we need are included on the page.
    assert b'Xpand Rally' in response_page_1.data
    assert b'Call of Duty' in response_page_1.data
    assert b'Nikopol: Secrets of the Immortals' in response_page_1.data

    assert b'Deadfall Adventures' in response_page_2.data
    assert b'Hexodius' in response_page_2.data
    assert b'Expeditions: Conquistador' in response_page_2.data

def test_e2e_games_page_with_order(client):
    # Check that we can retrieve the games page with order.
    response_game_id = client.get('/games?page=2&order=game_id')
    response_title = client.get('/games?page=2&order=title')
    response_publisher = client.get('/games?page=2&order=publisher')
    response_release_date = client.get('/games?page=2&order=release_date')
    response_price = client.get('/games?page=2&order=price')
    assert response_game_id.status_code == 200
    assert response_title.status_code == 200
    assert response_publisher.status_code == 200
    assert response_release_date.status_code == 200
    assert response_price.status_code == 200

    # Check that the first 3 games we need are included on the page.
    assert b'Deadfall Adventures' in response_game_id.data
    assert b'Hexodius' in response_game_id.data
    assert b'Expeditions: Conquistador' in response_game_id.data

    assert b'Alien Planet' in response_title.data
    assert b'Aliens vs. Ghosts' in response_title.data
    assert b'Alone In The Mars' in response_title.data

    assert b'Into the Pyramid' in response_publisher.data
    assert b"Gripper's Adventure" in response_publisher.data
    assert b'SC2KRender' in response_publisher.data

    assert b'VELONE' in response_release_date.data
    assert b'Gem Tower Defense 2' in response_release_date.data
    assert b"Darza's Dominion" in response_release_date.data

    assert b'MagiCats Builder (Crazy Dreamz)' in response_price.data
    assert b'Lumberjack VR' in response_price.data
    assert b'Google Spotlight Stories: Special Delivery' in response_price.data



# Test adding games to the favourite list




# Test logging out