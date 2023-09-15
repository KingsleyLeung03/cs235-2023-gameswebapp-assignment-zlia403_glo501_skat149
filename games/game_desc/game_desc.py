# ---------------------------------------
# require packages for all brueprint file
# ---------------------------------------
from flask import Blueprint, render_template, redirect, url_for, session, request

import games.adapters.repository as repo
import games.authentication.authentication as authentication
import games.authentication.services as services

# ---------------------------------------

import games.game_desc.services as services
game_desc_blueprint = Blueprint("game_desc_bp", __name__)

@game_desc_blueprint.route('/gameDescription/<game_id>', methods=["GET"])
def game_description(game_id):
        # check that recived value is integer
        try:
            game_id = int(game_id)
        except:
            return render_template("notFound.html", message=f"Invalid game ID!")
        game = None

            
        geners_list = services.get_genre_list(repo.repo_instance)
        publisher_list = services.get_publisher_list(repo.repo_instance)

        try:
            game = services.get_game(repo.repo_instance, game_id)
        except: # if game not found
            return render_template("notFound.html", message=f"game id: {game_id} is not found.",genres=geners_list,publishers=publisher_list)
        else: # if not error 
            return render_template('gameDescription.html', game=game,genres=geners_list,publishers=publisher_list)
        
