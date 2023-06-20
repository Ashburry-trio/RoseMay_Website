#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations

from flask_login import LoginManager
from flask import Flask
from website import db

DB_NAME: str = "database.db"

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SERVER_NAME'] = "www.mslscript.com"
app.secret_key = "AadaDADSASDASDSDAasdsda"
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
from website.views import views
from website.auth import auth
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(userid):
    try:
        return session.query(User).filter(User.id == userid).first()
    except models.DoesNotExist :
        return None

@app.before_first_request
def create_table():
    db.create_all()