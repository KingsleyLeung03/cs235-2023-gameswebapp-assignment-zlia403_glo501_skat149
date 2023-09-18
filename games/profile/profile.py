from flask import Blueprint, render_template, request
from games.domainmodel.model import *


import games.adapters.repository as repo
import games.profile.services as services

profile_blueprint = Blueprint("profile_bp", __name__)


@profile_blueprint.route('/profile', methods=['GET'])
def show_profile():

    # Use the testing profile for testing
    profile = services.get_profile(repo.repo_instance ,"demo_user")

    return render_template("profile.html", profile = profile)

