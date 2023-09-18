# ---------------------------------------
# require packages for all brueprint file
# ---------------------------------------
from flask import Blueprint, render_template, redirect, url_for, session, request

import games.adapters.repository as repo
import games.authentication.authentication as authentication

# ---------------------------------------

import games.genre_bases.services as services
from games.domainmodel.model import *
genre_bases_blueprint = Blueprint("genre_bases_bp", __name__)

games_per_page = 30

@genre_bases_blueprint.route('/genre/<target>', methods=["GET"])
def show_games_trial(target):
    # check if authenticated
    authenticated = authentication.check_authenticated()
    
    pagenum = request.args.get("page")
    order = request.args.get("order")

    if not order:
        order =""
    
    genres_list = services.get_genre_list(repo.repo_instance)
    
    for _genre in genres_list:
        if(_genre.genre_name == target):
            genre = _genre
    
    #if pagenum is not set then page is 1 else page is given value for invalid page
    if not pagenum:
        pagenum = 1
    else:
        try:
            pagenum = int(pagenum)
        except:
            return render_template("notFound.html", message=f"Invalid page value!", authenticated=authenticated)
        
    services.get_games_by_genre(repo.repo_instance,genre)

    num_games = services.get_number_of_games(repo.repo_instance)
    games = services.get_games(repo.repo_instance, games_per_page, pagenum, order)
    maxpage = services.get_max_page_num(num_games, games_per_page)
    pages = services.generate_page_list(pagenum, maxpage)
    option_of_order = ["game_id", "title", "publisher", "release_date", "price"]
    publisher_list = services.get_publisher_list(repo.repo_instance)

    page_info = {
        "number_of_games": num_games,
        "maxpage": maxpage,
        "current_display": services.get_current_display(num_games, games_per_page, pagenum),
        "current_page": pagenum,
        "current_order": order
    }

    return render_template(
        "genre.html",
        games=games,
        num_game=num_games,
        page_info=page_info,
        pages=pages,
        order_options=option_of_order,
        genres=genres_list,
        publishers=publisher_list,
        genre=genre,
        authenticated=authenticated
    )



