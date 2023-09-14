from flask import Blueprint, render_template, request

import games.adapters.repository as repo
import games.profile.services as services

profile_blueprint = Blueprint("profile_bp", __name__)


@profile_blueprint.route('/profile', methods=['GET'])
def show_profile():

    return render_template("profile.html")
