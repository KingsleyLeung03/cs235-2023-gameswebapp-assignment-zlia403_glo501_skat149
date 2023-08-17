from bisect import insort_left
from typing import List
import os

from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game, Genre, Publisher, Review
from games.adapters.datareader.csvdatareader import GameFileCSVReader

# errors
class GameNotFoundException(Exception):
    def __init__(self, message=None):
        pass

# reop class
class MemoryRepository(AbstractRepository):
    def __init__(self) -> None:
        super().__init__()
        self.__games: List[Game] = list()
        
    def add_game(self, game: Game):
        if isinstance(game, Game):
            # When inserting the game, keep the game list sorted alphabetically by the id.
            # Games will be sorted by game due to __lt__ method of the Game class.
            insort_left(self.__games, game)
            
    def get_game_list(self) -> List[Game]:
        return self.__games

    def get_number_of_games(self):
        return len(self.__games)
    
    def get_game_by_id(self, game_id: int) -> Game:
        if isinstance(game_id, int):
            for game in self.__games:
                if game.game_id == game_id:
                    # return str(game_id)
                    return game
            raise GameNotFoundException
        else:
            raise TypeError
        
    def get_game_title(self, game_obj: Game) -> str:
        return game_obj.title
        
    def get_game_price(self, game_obj: Game) -> float:
        return game_obj.price
    
    def get_geme_release_date(self, game_obj: Game) -> str:
        return game_obj.release_date
    
    def get_game_description(self, game_obj: Game) -> str:
        return game_obj.description
    
    def get_game_image_url(self, game_obj: Game) -> str:
        return game_obj.image_url
    
    def get_game_website_url(self, game_obj: Game) -> str:
        return game_obj.website_url
    
    def get_game_publisher(self, game_obj: Game) -> Publisher:
        return game_obj.publisher
    
    def get_game_genres(self, game_obj: Game) -> List[Genre]:
        return game_obj.genres
        
    def get_game_reviews(self, game_obj: Game) -> List[Review]:
        return game_obj.reviews
        