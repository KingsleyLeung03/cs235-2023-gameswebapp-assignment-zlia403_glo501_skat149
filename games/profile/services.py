from games.adapters.repository import AbstractRepository

class NonExistentGameException(Exception):
    pass


class UnknownPageException(Exception):
    pass