import abc
from typing import List

from games.domainmodel.model import *

repo_instance = None

class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class RepositoryException(Exception):
    def __init__(self, message=None):
        print(f'RepositoryException: {message}')


class AbstractRepository(abc.ABC):
    
    @abc.abstractmethod
    def add_game(self, game: Game):
        """ Add a game to the repository list of games. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_games(self) -> int:
        """ Returns a number of games exist in the repository. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_game_list(self) -> List[Game]:
        """" Returns the list of games. """
        raise NotImplementedError
    
    # game atritbutes 
    
    @abc.abstractmethod
    def get_game_by_id(self, game_id: int) -> Game:
        """" get game by id. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_game_title(self, game_obj: Game) -> str:
        """" get title of game by id. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_game_price(self, game_obj: Game) -> float:
        """" get price of the game by id. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_geme_release_date(self, game_obj: Game) -> str:
        """" get release_date of the game by id. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_game_description(self, game_obj: Game) -> str:
        """" get description of the game by id. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_game_image_url(self, game_obj: Game) -> str:
        """" get image_url of the game by id. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_game_website_url(self, game_obj: Game) -> str:
        """" get website_url of the game by id. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_game_publisher(self, game_obj: Game) -> Publisher:
        """" get auther of game by id. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_game_genres(self, game_obj: Game) -> List[Genre]:
        """" get list of genres of the game by id. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_game_reviews(self, game_obj: Game) -> List[Review]:
        """" get list of reviews of the game by id. """
        raise NotImplementedError
    
    #get games by xxx 
    
    @abc.abstractmethod
    def get_games_by_publisher(self, publisher: Publisher) -> List[Game]:
        """" get list of game by publisher. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_games_by_genre(self, genre: Genre) -> List[Game]:
        """" get list of game by genre. """
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_games_by_review(self, review: Review) -> List[Game]:
        """" get list of game by review. """
        raise NotImplementedError
    
    
    # about genres class
    
    # about Publisher class
    
    # about Review class 
    

    
    
    