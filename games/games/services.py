from typing import List, Iterable
from games.adapters.repository import AbstractRepository
from games.domainmodel.model import Game

class NonExistentGameException(Exception):
    pass


class UnknownPageException(Exception):
    pass


def get_games(repo: AbstractRepository, range: int,  pagenum: int):
    if not isinstance(range, int) and not isinstance(pagenum, int) and pagenum<1:
        raise UnknownPageException
    
    start_index = range*(pagenum-1)
    end_index = range*pagenum
    
    if end_index > get_number_of_games(repo) -1:
        end_index = get_number_of_games(repo) -1
         
    games = repo.get_game_list()[start_index: end_index]
    game_dicts = []
    for game in games:
        game_dict = {
            "game_id": game.game_id,
            "title": game.title,
            "image_url": game.image_url,
            "price": game.price
        }
        game_dicts.append(game_dict)
    
    return game_dicts
  
def get_max_page_num(number_of_games: int, games_per_page: int) -> int:
    if isinstance(number_of_games, int) and isinstance(games_per_page, int):    
        # max page number is #of games/ game par page if divisible, if not +1 
        maxpage = number_of_games//games_per_page 
        if not number_of_games % games_per_page == 0:
            maxpage += 1
        return maxpage
    
    


def get_number_of_games(repo: AbstractRepository) -> int:
    return repo.get_number_of_games()


