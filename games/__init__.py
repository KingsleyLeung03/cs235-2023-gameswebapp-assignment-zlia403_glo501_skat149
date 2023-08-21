"""Initialize Flask app."""

from flask import Flask, render_template, request

# TODO: Access to the games should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
from games.domainmodel.model import Game

# this line must be deleted
from games.adapters.datareader.csvdatareader import GameFileCSVReader

import games.adapters.repository as repo
from games.adapters.memory_repository import populate
from games.adapters.memory_repository import MemoryRepository


# TODO: Access to the games should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!

# this lines must be removed
csvData = GameFileCSVReader("games/adapters/data/games.csv")
csvData.read_csv_file()

def create_some_game():
    some_game = Game(1, "Call of Duty® 4: Modern Warfare®")
    some_game.release_date = "Nov 12, 2007"
    some_game.price = 9.99
    some_game.description = "The new action-thriller from the award-winning team at Infinity Ward, the creators of " \
                            "the Call of Duty® series, delivers the most intense and cinematic action experience ever. "
    some_game.image_url = "https://cdn.akamai.steamstatic.com/steam/apps/7940/header.jpg?t=1646762118"
    return some_game



def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)
    
    
    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    # fill the repository from the provided CSV file
    populate(repo.repo_instance)

    @app.route('/')
    def home():
        # some_game = create_some_game()
        # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
        publisher_list = repo.repo_instance.get_publisher_list()
        geners_list = repo.repo_instance.get_genre_list()
        return render_template("layout.html",genres=geners_list,publishers=publisher_list)

    @app.route("/layout")
    def layout_page():

        publisher_list = repo.repo_instance.get_publisher_list()
        geners_list = repo.repo_instance.get_genre_list()
        return render_template("layout.html",genres=geners_list,publishers=publisher_list)
    
    
    with app.app_context():
        # Register the game_desc blueprint to the app instance.
        from .game_desc import game_desc
        app.register_blueprint(game_desc.game_desc_blueprint)
        
        # Register the games blueprint to the app instance.
        from .games import games
        app.register_blueprint(games.games_blueprint)

        # Register the search blueprint to the app instance.
        from .search import search
        app.register_blueprint(search.search_blueprint)

        # Register the genre_bases blueprint to the app instance.
        from .genre_bases import genre_bases
        app.register_blueprint(genre_bases.genre_bases_blueprint)
    
        # Register the genre_bases blueprint to the app instance.
        from .publisher_bases import publisher_bases
        app.register_blueprint(publisher_bases.publisher_bases_blueprint)



    return app