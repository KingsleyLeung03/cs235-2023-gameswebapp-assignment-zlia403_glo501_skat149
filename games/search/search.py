from flask import Blueprint, render_template, request
# from games.adapters.datareader.csvdatareader import GameFileCSVReader

import games.adapters.repository as repo
import games.search.services as services
search_blueprint = Blueprint("game_search_bp", __name__)
games_per_page = 30



@search_blueprint.route('/search/<target>/<type>', methods=["GET"])
def show_games(target,type):
    ##
    pagenum = request.args.get("page")
    order = request.args.get("order")

    if not order:
        order =""
    
    genres_list = services.get_genre_list(repo.repo_instance)
    publisher_list = services.get_publisher_list(repo.repo_instance)
    
    if (type == "publisher"):
        print(services.get_games_by_publisher(repo.repo_instance,target))
    elif (type == "genre"): 
        print(services.get_games_by_genre(repo.repo_instance,target))
    else: 
        print(services.get_games_by_title(repo.repo_instance,target))
    #print(type)



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

    print(games_per_page, pagenum, order,maxpage,num_games,pages)

    page_info = {
        "number_of_games": num_games,
        "maxpage": maxpage,
        "current_display": services.get_current_display(num_games, games_per_page, pagenum),
        "current_page": pagenum,
        "current_order": order
    }
    
    print(games)
    
    return render_template("search.html", games=games, num_game=num_games, page_info=page_info, pages=pages, order_options=option_of_order,genres=genres_list,publishers=publisher_list,type=type,target=target)
    #return render_template("genre.html", games=games, num_game=num_games, page_info=page_info, pages=pages, order_options=option_of_order,genres=genres_list,publishers=publisher_list,genre=target)

