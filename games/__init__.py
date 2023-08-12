"""Initialize Flask app."""

from flask import Flask, render_template, request

# TODO: Access to the games should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
from games.domainmodel.model import Game
from games.adapters.datareader.csvdatareader import GameFileCSVReader


# TODO: Access to the games should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!

csvData = GameFileCSVReader("games/adapters/data/games.csv")
csvData.read_csv_file()

def create_some_game():
    some_game = Game(1, "Call of Duty® 4: Modern Warfare®")
    some_game.release_date = "Nov 12, 2007"
    some_game.price = 9.99
    some_game.description = "The new action-thriller from the award-winning team at Infinity Ward, the creators of " \
                            "the Call of Duty® series, delivers the most intense and cinematic action experience ever. "
    some_game.image_url = "https://cdn.akamai.steamstatic.com/steam/apps/7940/header.jpg?t=1646762118"
    return some_game



def create_app():
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    @app.route('/')
    def home():
        some_game = create_some_game()
        # Use Jinja to customize a predefined html page rendering the layout for showing a single game.
        return render_template('layout.html')
    
    @app.route("/gameDescription/<game_id>", methods=["GET"])
    def game_description(game_id):
        # game_id = request.args.get("game_id")
        # check that recived value is integer
        try:
            game_id = int(game_id)
        except:
            return "agument error"
        
        for game in csvData.dataset_of_games:
            if game.game_id == game_id:
                # return str(game_id)
                return render_template('gameDescription.html', game=game)
        return (game_id, "not found")
        
    @app.route("/layout")
    def layout_page():
        return render_template("layout.html")


    @app.route("/test")
    def test_page():
        return "test page"

    
    
    
    @app.route('/games')
    def show_listof_games():
        return render_template("games.html", games=csvData.dataset_of_games)
    

    @app.route('/search')
    def search_games():
        target = "the".lower()
        result = []
        for game in csvData.dataset_of_games:
            if str(target) in game.title.lower() or str(target) in game.publisher.publisher_name.lower() or str(target) in str(game.description).lower():
                if game not in result:
                    result.append(game)
            for genre in game.genres:
                if str(target) in genre.genre_name.lower() and game not in result:
                    result.append(game)

        return render_template("games.html", games=result)


    return app
