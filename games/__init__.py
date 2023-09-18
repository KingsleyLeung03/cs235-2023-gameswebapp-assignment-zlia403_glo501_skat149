"""Initialize Flask app."""
from pathlib import Path
from flask import Flask, render_template, request


import games.adapters.repository as repo
from games.adapters.memory_repository import populate
from games.adapters.memory_repository import MemoryRepository


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)
    
    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('games') / 'adapters' / 'data'
    
    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']
    
    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    # fill the repository from the provided CSV file


    populate(data_path, repo.repo_instance)

    # Demo user, only for testing profile page
    demo_user = User("demo_user", "password")
    repo.repo_instance.add_user(demo_user)
    demo_game_1 = repo.repo_instance.get_game_by_id(7940)
    demo_game_2 = repo.repo_instance.get_game_by_id(1228870)
    demo_game_3 = repo.repo_instance.get_game_by_id(311120)
    demo_review_1 = Review(demo_user, demo_game_1, 1, "Bad game!")
    demo_review_2 = Review(demo_user, demo_game_2, 5, "Good game!")
    demo_user.add_review(demo_review_1)
    demo_user.add_review(demo_review_2)
    demo_user.add_favourite_game(demo_game_2)
    demo_user.add_favourite_game(demo_game_3)

    
    with app.app_context():
        # Register the home blueprint to the app instance.
        from .home import home
        app.register_blueprint(home.home_blueprint)

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

        # Register the profile blueprint to the app instance.
        from .profile import profile
        app.register_blueprint(profile.profile_blueprint)

        # Register the profile blueprint to the app instance.
        from .favourites import favourites
        app.register_blueprint(favourites.favourites_blueprint)


    return app