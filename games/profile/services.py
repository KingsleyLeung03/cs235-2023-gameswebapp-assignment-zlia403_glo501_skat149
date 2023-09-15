from games.adapters.repository import AbstractRepository
from games.domainmodel.model import *


class NonExistentGameException(Exception):
    pass


class UnknownPageException(Exception):
    pass

def get_profile(repo: AbstractRepository, username: str):
    if not isinstance(username, str):
        raise TypeError

    user = repo.get_user(username)
    profile_dict = {
        "username": user.username,
        "user_reviews": user.reviews,
        "user_favourite": user.favourite_games
    }
    return profile_dict






