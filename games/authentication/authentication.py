from flask import Blueprint, render_template, redirect, url_for, session, request
# from games.adapters.datareader.csvdatareader import GameFileCSVReader

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import games.adapters.repository as repo
import games.games.services as services
authentication_blueprint  = Blueprint("authentication_bp", __name__)

@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    return render_template(
        "authentication/credentials.html", 
        title="Register",
        form=form,
        handler_url=url_for('authentication_bp.register')
        
    )


class RegistrationForm(FlaskForm):
    user_name = StringField(
        'Username', 
        validators=[
            DataRequired(message='Your user name is required'),
            Length(min=3, message='Your user name is too short')
        ],
        render_kw={
            "placeholder": "User name is not case sensitive",
            "class": "text-input"
        }
    )
    
    password = PasswordField(
        'Password', 
        validators=[
            DataRequired(message='Your password is required')
        ],
        render_kw={
            "placeholder": "Password",
            "class": "text-input", 
            "size": "40"
        }
    )
    
    submit = SubmitField('Register', render_kw={"class": "form_submit_button"})