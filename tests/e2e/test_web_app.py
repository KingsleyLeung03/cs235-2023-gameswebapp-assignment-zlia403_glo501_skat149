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

# def test_e2e_games_page_with_order(client):
    # Check that we can retrieve the games page with order.



# Test adding games to the favourite list




# Test logging out