from flask import Blueprint, render_template
# here must be memory repo import
# this must be replaced with service layer file
from games.adapters.datareader.csvdatareader import GameFileCSVReader

games_blueprint = Blueprint("games_bp", __name__)

# this also must be replaced 
csvData = GameFileCSVReader("games/adapters/data/games.csv")
csvData.read_csv_file()

@games_blueprint.route('/games')
def show_games():
    # this must be replaced by data from momery repo
    return render_template("games.html", games=csvData.dataset_of_games)
