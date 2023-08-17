from flask import Blueprint, render_template, request
# here must be memory repo import
# this must be replaced with service layer file
# from games.adapters.datareader.csvdatareader import GameFileCSVReader

import games.adapters.repository as repo
import games.games.services as services
games_blueprint = Blueprint("games_bp", __name__)

games_per_page = 30



@games_blueprint.route('/games')
def show_games():
    pagenum = request.args.get("page")
    #of pagenum is not set then page is 1 else page is given value for invalid page
    if not pagenum:
        pagenum = 1
    else:
        try:
            pagenum = int(pagenum)
        except:
            return render_template("notFound.html", message=f"Invalid page value!")
    
    # this must be replaced by data from momery repo
    num_games = services.get_number_of_games(repo.repo_instance)
    games = services.get_games(repo.repo_instance, games_per_page, pagenum)
    maxpage = services.get_max_page_num(num_games, games_per_page)
    
    return render_template("games.html", games=games, num_game=num_games, pagenum=pagenum, pages=maxpage)

