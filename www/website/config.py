from flask import (
    Blueprint, render_template, make_response, Response, jsonify, redirect, send_file, url_for
    )
from flask import request, flash, redirect, session
from flask_app import gk, limiter
from os.path import expanduser
from os import path
from time import time as ctime
import os
from configparser import ConfigParser
import hashlib
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Regexp
from website import save_user, load_users_ini

config = Blueprint('config', __name__, template_folder='templates', static_folder='static')

class ServerForm(FlaskForm):
    # Proxy Listening Port (3000-5000, excluding 3128)
    port = IntegerField(
        'Proxy Listening Port Number (3000-5000, excluding 3128, unique system wide):',
        validators=[
            DataRequired(),
            NumberRange(min=3000, max=5000, message="Port must be between 3000 and 5000")
        ]
    )

    # DCC Chat Server Port (1400-1900)
    dcc = IntegerField(
        'DCC Chat Server (1400-1900, must also be unique system wide):',
        validators=[
            DataRequired(),
            NumberRange(min=1400, max=1900, message="DCC port must be between 1400 and 1900")
        ]
    )

    # Identd Response (alphanumeric, 0-15 chars, must start with a letter)
    identd = StringField(
        'Identd Response:',
        validators=[
            DataRequired(),
            Regexp(r'^[a-zA-Z][a-zA-Z0-9]{0,15}$', message="Must start with a letter, max 16 characters")
        ]
    )

    # Email Address (validation pattern for email)
    email = EmailField(
        'Email:',
        validators=[
            DataRequired(),
            Email(message="Invalid email address"),
            Length(min=5, max=34, message="Email must be between 5 and 34 characters")
        ]
    )

    # Username (3-24 characters, disabled in the form)
    username = StringField(
        'Username:',
        validators=[
            Regexp(r'^[a-zA-Z][a-zA-Z0-9_-]{3,24}$', message="Invalid username"),
            Length(min=3, max=24)
        ]
    )

    # Password (8-24 characters, alphanumeric, starts with letter/number)
    password = PasswordField(
        'Password:',
        validators=[
            DataRequired(),
            Regexp(r'^[a-zA-Z0-9][a-zA-Z0-9_-]{7,23}$', message="Password must be 8-24 characters long")
        ]
    )

    # Submit button
    submit = SubmitField('Apply Changes')


@config.route('/config/server.html', methods=['GET','POST'])
@config.route('/config/service.html', methods=['GET','POST'])
def config_server():
    """Configure proxy listening port, dcc chat server port, username, password,
    identd response, and email.

    """
    gk.report()
    if 'logged_in' in session.keys() and session['logged_in'] == True:
        pass
    else:
        return redirect('/index.html', code=307)

    form = ServerForm()
    if form.validate_on_submit():
        # Process form data, for example:
        server_port = form.port.data
        dcc_port = form.dcc.data
        identd_resp = form.identd.data
        email_addr = form.email.data
        username = form.username.data
        password = form.password.data
        # Save or process the data
        return "Form submitted successfully!"
    return render_template('config/server.html', form=form)