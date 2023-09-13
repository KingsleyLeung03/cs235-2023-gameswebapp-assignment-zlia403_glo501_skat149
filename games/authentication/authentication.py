from flask import Blueprint, render_template, redirect, url_for, session, request
# from games.adapters.datareader.csvdatareader import GameFileCSVReader

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from password_validator import PasswordValidator

from functools import wraps

import games.adapters.repository as repo
import games.authentication.services as services
authentication_blueprint  = Blueprint("authentication_bp", __name__)

@authentication_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_name_not_unique = None
    
    if form.validate_on_submit():
        # Successful POST, i.e. the user name and password have passed validation checking.
        # Use the service layer to attempt to add the new user.
        try:
            services.add_user(form.user_name.data, form.password.data, repo.repo_instance)
            return redirect(url_for(authentication_blueprint.login)) # only when no error occur
        
        except services.NameNotUniqueException:
            user_name_not_unique = "This user name is already taken - please enter another"
            
    return render_template(
        "authentication/credentials.html", 
        title="Register",
        user_name_error_message=user_name_not_unique,
        form=form,
        handler_url=url_for('authentication_bp.register')
        
    )




class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


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
            DataRequired(message='Your password is required'),
            PasswordValid()
        ],
        render_kw={
            "placeholder": "Password",
            "class": "text-input", 
            "size": "40"
        }
    )
    
    submit = SubmitField('Register', render_kw={"class": "form_submit_button"})