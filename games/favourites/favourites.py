from flask import Blueprint, render_template, request, session
# from games.adapters.datareader.csvdatareader import GameFileCSVReader

import games.adapters.repository as repo
import games.favourites.services as services
import games.authentication.authentication as authentication
favourites_blueprint = Blueprint("favourites_bp", __name__)

games_per_page = 10



@favourites_blueprint.route('/favourites', methods=['GET'])
def show_games():
    authenticated = authentication.check_authenticated()
    user_name = session["User_name"]
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
        
    
    num_games = services.get_number_of_games(repo.repo_instance, user_name)
    games = services.get_games(repo.repo_instance, games_per_page, pagenum, user_name, order)
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
    
    return render_template("favourites.html", games=games, num_game=num_games, page_info=page_info, pages=pages, order_options=option_of_order,genres=geners_list,publishers=publisher_list,authenticated=authenticated)

@favourites_blueprint.route("/favourites/change_favourite/<game_id>")
def change_favourite(game_id: str):
    user_name = None
    user_name = session["User_name"]
    services.change_favourite(repo.repo_instance,(game_id),user_name)
    print("clicked")
    return show_games()
