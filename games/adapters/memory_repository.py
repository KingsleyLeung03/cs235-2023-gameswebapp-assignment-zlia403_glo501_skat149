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
    # about Game object
    
    def __init__(self) -> None:
        super().__init__()
        self.__games: List[Game] = list()
        self.__genres: List[Genre] = list()
        self.__publishers: List[Publisher] = list()
        # self.__reviews: List[Review] = list()
        self.__games_search: List[Game] = list()
        self.__genres_filter: List[Genre] = list()
        self.__publishers_filter: List[Publisher] = list()
        
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
    
    def get_range_of_game_list(self, start: int, end: int, order: str = "game_id") -> List[Game]:
        if isinstance(start, int) and isinstance(end, int) and isinstance(order, str):
            gamelist = self.get_game_list()
            
            if order == "game_id":
                gamelist.sort(key= lambda game: game.game_id)
            elif order == "title":
                gamelist.sort(key=lambda game: game.title)
            elif order == "publisher":
                gamelist.sort(key=lambda game: game.publisher.publisher_name)
            elif order == "release_date":
                gamelist.sort(key=lambda game: game.release_date)
            elif order == "price":
                gamelist.sort(key=lambda game: game.price)
            else: 
                gamelist.sort(key= lambda game: game.game_id)
            
            
            gamelist = gamelist[start:end]
            return gamelist
            
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
    
    def get_games_by_genre(self, genre: Genre) -> List[Game]:
        if isinstance(genre, Genre):
            game_list: List[Game] = list()
            
            # look for the games that have the genre from arg
            for game in self.__games:
                if genre in game.genres:
                    insort_left(game_list, game)
                    
            return game_list
        
    def get_games_by_publisher(self, publisher: Publisher) -> List[Game]:
        if isinstance(publisher, Publisher):
            game_list: List[Game] = list()
            
            # look for games that have same publisher form arg
            for game in self.__games:
                if publisher == game.publisher:
                    insort_left(game_list, game)
            
            return game_list
        
            
    # about Genre class

    def add_genre(self, genre: Genre):
        if isinstance(genre, Genre):
            insort_left(self.__genres, genre)
            
    def get_genre_list(self) -> List[Game]:
        return self.__genres

    def get_number_of_genres(self) -> int:
        return len(self.__genres)
    
    
    # about Publisher class
    

    def add_publisher(self, publisher: Publisher):
        if isinstance(publisher, Publisher):
            insort_left(self.__publishers, publisher)

    def get_number_of_publisher(self) -> int:
        return len(self.__publishers)
    
    def get_publisher_list(self) -> List[Game]:
        return self.__publishers
    
    def get_number_of_search_games(self, target: str) -> int:
        return len(self.__games)
            
    
# add all game data to the memory repo obj using datareader
def populate(repo: AbstractRepository):
    dir_name = os.path.dirname(os.path.abspath(__file__))
    games_file_name = os.path.join(dir_name, "data/games.csv")
    reader = GameFileCSVReader(games_file_name)

    reader.read_csv_file()

    games = reader.dataset_of_games
    genres = reader.dataset_of_genres
    publishers = reader.dataset_of_publishers
    # reviews = reader.dataset

    # Add games to the repo
    for game in games:
        repo.add_game(game)
        
    for genre in genres:
        repo.add_genre(genre)
        
    for publisher in publishers:
        repo.add_publisher(publisher)
        