from flask import Blueprint, render_template
import games.adapters.repository as repo

layout_blueprint = Blueprint("layout_bp", __name__)


@layout_blueprint.route('/')
@layout_blueprint.route("/layout")
def layout():
    # some_game = create_some_game()
    # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
    publisher_list = repo.repo_instance.get_publisher_list()
    genres_list = repo.repo_instance.get_genre_list()
    return render_template("layout.html", genres=genres_list, publishers=publisher_list)
