"""Initialize Flask app."""
from pathlib import Path
from flask import Flask, render_template, request

#for test 
from games.domainmodel.model import *

from games.adapters.memory_repository import populate
from games.adapters.memory_repository import MemoryRepository
from games.adapters.orm import metadata, map_model_to_tables

# imports from SQLAlchemy
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

import games.adapters.repository as repo
from games.adapters.database_repository import SqlAlchemyRepository
#from games.adapters.repository_populate import populate
from games.adapters.orm import metadata, map_model_to_tables

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


    #SQL 
    database_uri = 'sqlite:///games.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_ECHO'] = True  # echo SQL statements - useful for debugging

    # Create a database engine and connect it to the specified database
    database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                    echo=False)

    # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)

    # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
    repo.repo_instance = SqlAlchemyRepository(session_factory)
    data_path = Path('games') / 'adapters' / 'data'

    if len(inspect(database_engine).get_table_names()) == 0:
        print("REPOPULATING DATABASE...")
        # For testing, or first-time use of the web application, reinitialise the database.
        clear_mappers()
        # Conditionally create database tables.
        metadata.create_all(database_engine)
        # Remove any data from the tables.
        for table in reversed(metadata.sorted_tables):
            with database_engine.connect() as conn:
                conn.execute(table.delete())

        # Generate mappings that map domain model classes to the database tables.
        map_model_to_tables()

        populate(data_path, repo.repo_instance)
        print("REPOPULATING DATABASE... FINISHED")

    else:
        # Solely generate mappings that map domain model classes to the database tables.
        map_model_to_tables()



    # read blueprint
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
