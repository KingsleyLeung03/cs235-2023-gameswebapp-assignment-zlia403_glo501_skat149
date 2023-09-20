from flask import Blueprint, render_template, request, redirect, url_for
from games.domainmodel.model import *


import games.adapters.repository as repo
import games.profile.services as services

profile_blueprint = Blueprint("profile_bp", __name__)


@profile_blueprint.route('/profile', methods=['GET'])
def show_profile():

    # Use the testing profile for testing
    profile = services.get_profile(repo.repo_instance ,"demo_user")

    return render_template("profile.html", profile = profile)

@profile_blueprint.route('/profile/remove_favourite/<game_id>', methods=['GET'])
def remove_favourite(game_id):

    # Use the testing profile for testing
    services.remove_favourite(repo.repo_instance, "demo_user", int(game_id))

    return redirect(url_for("profile_bp.show_profile"))