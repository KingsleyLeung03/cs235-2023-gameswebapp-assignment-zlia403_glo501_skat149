from typing import List, Iterable
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game

class NonExistentGameException(Exception):
    pass


class UnknownPageException(Exception):
    pass


def get_game(repo: AbstractRepository, game_id: int):
    if not isinstance(game_id, int):
        raise TypeError
    
    game_obj = repo.get_game_by_id(game_id)

    # Check the review numbers first to avoid ZeroDivisionError, then add to the dictionary
    if (len(game_obj.reviews) > 0):
        average_rating = round(sum(review.rating for review in game_obj.reviews) / len(game_obj.reviews), 1)
    else:
        average_rating = 0

    game = {
        "title": game_obj.title,
        "image_url": game_obj.image_url,
        "release_date": game_obj.release_date,
        "price": game_obj.price,
        "publisher_name": game_obj.publisher.publisher_name,
        # "rating": game_obj.reviews.rating,
        "website_url": game_obj.website_url,
        "genres": [genre.genre_name for genre in game_obj.genres],
        "description": game_obj.description,
        "game_reviews": game_obj.reviews,
        "num_game_reviews": len(game_obj.reviews),
        "game_reviews_average_rating": average_rating

    }
    
    return game
    
