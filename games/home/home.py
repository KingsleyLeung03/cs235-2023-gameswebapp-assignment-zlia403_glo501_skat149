# ---------------------------------------
# require packages for all brueprint file
# ---------------------------------------
from flask import Blueprint, render_template, redirect, url_for, session, request

import games.adapters.repository as repo
import games.authentication.authentication as authentication

# ---------------------------------------

home_blueprint = Blueprint("home_bp", __name__)


@home_blueprint.route('/', methods=['GET'])
@home_blueprint.route("/home", methods=['GET'])
def home():
    # check if authenticated
    authenticated = authentication.check_authenticated()
    
    # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
    publisher_list = repo.repo_instance.get_publisher_list()
    genres_list = repo.repo_instance.get_genre_list()
    return render_template(
        "home.html",
        genres=genres_list,
        publishers=publisher_list,
        authenticated=authenticated
    )
