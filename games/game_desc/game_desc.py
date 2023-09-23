# ---------------------------------------
# require packages for all brueprint file
# ---------------------------------------
from flask import Blueprint, render_template, redirect, url_for, session, request

import games.adapters.repository as repo
import games.authentication.authentication as authentication
from games.authentication.authentication import login_required

# ---------------------------------------
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, ValidationError

import games.game_desc.services as services
game_desc_blueprint = Blueprint("game_desc_bp", __name__)

@game_desc_blueprint.route('/gameDescription/<game_id>', methods=["GET"])
def game_description(game_id):
    # check if authenticated
    authenticated = authentication.check_authenticated()
    form = ReviewForm()
    game = None

        
    geners_list = services.get_genre_list(repo.repo_instance)
    publisher_list = services.get_publisher_list(repo.repo_instance)
    # review_list = services.get_user_review(repo.repo_instance,game_id)
    # Move down this code, or it will raise GameNotFoundException if game is not exist

    favourite_list = False

    # print(review_list)

    try:
        game_id = int(game_id)
        game = services.get_game(repo.repo_instance, game_id)
    except: # if game not found 
        return render_template(
            "notFound.html",
            message=f"game id: {game_id} is not found.",
            genres=geners_list,
            publishers=publisher_list,
            authenticated=authenticated,
            favourite_list = favourite_list
        )
        
    else: # if not error
        
        if "User_name" in session:
            user_name = session["User_name"]
            favourite_list = services.get_favourite_list(repo.repo_instance,game_id,user_name)
        
        # Process inout from form
        if form.validate_on_submit():
            print("submit")
            # Successful POST, i.e. the user name and password have passed validation checking.
            # Use the service layer to attempt to add the new user.
            
            #services.review(repo.repo_instance,int(game_id),int(form.rate.data),form.comment.data,user_name)
        print("form")
        print(form.comment.data)


        review_list = services.get_user_review(repo.repo_instance, game_id)
                
        return render_template(
            'gameDescription.html',
            game=game,
            genres=geners_list,
            publishers=publisher_list,
            authenticated=authenticated,
            review_list=review_list,
            form=form,
            favourite_list = favourite_list
        )
    

@game_desc_blueprint.route('/review/<game_id>/<rate>/<comment>', methods=["GET"])
@login_required
def review(game_id: int, rate: int, comment: str):
    user_name = None
    if "User_name" in session:
        user_name = session["User_name"]
        print("review")
        print(comment)
        print(comment=="style.css")
        if (comment!="style.css"):
            services.review(repo.repo_instance,int(game_id),int(rate),comment,user_name)
        return game_description(game_id)
    else :
        print("No user login yet")
        return game_description(game_id)


@game_desc_blueprint.route("/gameDescription/change_favourite/<game_id>")
@login_required
def change_favourite(game_id: str):
    user_name = None
    if "User_name" in session:
        user_name = session["User_name"]
        services.change_favourite(repo.repo_instance,(game_id),user_name)
        print("clicked")
        return game_description(game_id)
    else:
        #set a error message?
        print(type(game_id))
        print(game_id)
        return game_description(game_id)

class ReviewForm(FlaskForm):
    comment = TextAreaField('Comment', render_kw={"rows": 7, "cols": 100})
    rate = RadioField("Rating")
    submit = SubmitField('Submit')
