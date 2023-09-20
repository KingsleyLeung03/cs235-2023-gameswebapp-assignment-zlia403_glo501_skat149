# ---------------------------------------
# require packages for all brueprint file
# ---------------------------------------
from flask import Blueprint, render_template, redirect, url_for, session, request

import games.adapters.repository as repo
import games.authentication.authentication as authentication

# ---------------------------------------

import games.games.services as services
games_blueprint = Blueprint("games_bp", __name__)

games_per_page = 30

order_c = None
pagenum_c = None

@games_blueprint.route('/games', methods=['GET'])
def show_games(reflesh=None):
    pagenum = request.args.get("page")
    order = request.args.get("order")
    
    # check if authenticated
    authenticated = authentication.check_authenticated()
    
    if(reflesh==None):
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
        global order_c, pagenum_c
        order_c = order
        pagenum_c = pagenum
    
    else:
        order = order_c
        pagenum = pagenum_c
        
    favourite_list = []
    if "User_name" in session:
        user_name = session["User_name"]
        favourite_list = services.get_favourite_list(repo.repo_instance,user_name)

    print(favourite_list)

    num_games = services.get_number_of_games(repo.repo_instance)
    games = services.get_games(repo.repo_instance, games_per_page, pagenum, order)
    maxpage = services.get_max_page_num(num_games, games_per_page)
    pages = services.generate_page_list(pagenum, maxpage)
    option_of_order = ["game_id", "title", "publisher", "release_date", "price"]
    geners_list = services.get_genre_list(repo.repo_instance)
    publisher_list = services.get_publisher_list(repo.repo_instance)
    # print(games_per_page, pagenum, order,maxpage,num_games,pages) # I thing someone added for debag but I commented out to not confuse output from program
    
    page_info = {
        "number_of_games": num_games,
        "maxpage": maxpage,
        "current_display": services.get_current_display(num_games, games_per_page, pagenum),
        "current_page": pagenum,
        "current_order": order
    }
    
    return render_template(
        "games.html",
        games=games,
        num_game=num_games,
        page_info=page_info,
        pages=pages,
        order_options=option_of_order,
        genres=geners_list,
        publishers=publisher_list,
        authenticated=authenticated,
        favourite_list=favourite_list
    )

@games_blueprint.route("/game/change_favourite/<game_id>")
def change_favourite(game_id: str):
    user_name = None
    if "User_name" in session:
        user_name = session["User_name"]
        services.change_favourite(repo.repo_instance,(game_id),user_name)
        print("clicked")
    else:
        #set a error message?
        print(type(game_id))
        print(game_id)
    return show_games(True)