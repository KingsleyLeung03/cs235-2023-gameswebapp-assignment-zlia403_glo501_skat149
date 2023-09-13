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


def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)
    
    
    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    # fill the repository from the provided CSV file
    populate(repo.repo_instance)
    
    with app.app_context():
        # Register the layout blueprint to the app instance.
        from .layout import layout
        app.register_blueprint(layout.layout_blueprint)

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
        
        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)



    return app