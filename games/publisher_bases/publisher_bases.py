# ---------------------------------------
# require packages for all brueprint file
# ---------------------------------------
from flask import Blueprint, render_template, redirect, url_for, session, request

import games.adapters.repository as repo
import games.authentication.authentication as authentication
import games.authentication.services as services

# ---------------------------------------

import games.publisher_bases.services as services
publisher_bases_blueprint = Blueprint("publisher_bases_bp", __name__)

games_per_page = 30



@publisher_bases_blueprint.route('/publisher', methods=['GET'])
def show_games():
    pagenum = request.args.get("page")
    order = request.args.get("order")
    
    if not order:
        order =""
    
    #if pagenum is not set then page is 1 else page is given value for invalid page
    if not pagenum:
        pagenum = 1
    else:
        try:
            pagenum = int(pagenum)
        except:
            return render_template("notFound.html", message=f"Invalid page value!")
        
    
    num_games = services.get_number_of_games(repo.repo_instance)
    games = services.get_games(repo.repo_instance, games_per_page, pagenum, order)
    maxpage = services.get_max_page_num(num_games, games_per_page)
    pages = services.generate_page_list(pagenum, maxpage)
    option_of_order = ["game_id", "title", "publisher", "release_date", "price"]
    geners_list = services.get_genre_list(repo.repo_instance)
    publisher_list = services.get_publisher_list(repo.repo_instance)
    
    
    page_info = {
        "number_of_games": num_games,
        "maxpage": maxpage,
        "current_display": services.get_current_display(num_games, games_per_page, pagenum),
        "current_page": pagenum,
        "current_order": order
    }
    
    return render_template("games.html", games=games, num_game=num_games, page_info=page_info, pages=pages, order_options=option_of_order,genres=geners_list,publishers=publisher_list)

