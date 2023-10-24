#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations

from datetime import timedelta
from flask import Flask, request
from flask_session import Session
from flask_gatekeeper import GateKeeper
from os.path import expanduser
import sys

key: str
def make_key():
    global key
    try:
        with open(expanduser("~/secret.txt"), 'r') as fp:
            key = fp.read()
            key = bytes(key.split('\n')[0].strip(), 'utf-8')
            if not key:
                raise NameError('Key is empty space! This is wrong.')
    except (NameError, FileNotFoundError):
        import secrets
        with open(expanduser("~/secret.txt"), 'w') as fp:
            LETTERS = secrets.token_urlsafe(55)
            fp.write(LETTERS)
            key = bytes(LETTERS, 'utf-8')
        del LETTERS
        del secrets
make_key()
app = Flask(__name__)
app.secret_key = key or b"Jsd1232f3oasdfsd4FDSEf;asdfjkXCVBEUK:ajkdf12u3y908)(*@#$*(,.;"
app.config['SERVER_NAME'] = "www.mslscript.com"
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_FILE_DIR"] = expanduser('~/flask_session_cache')
app.config["SESSION_TYPE"] = "filesystem"     #  or file
app.config['SESSION_FILE_THRESHOLD'] = 250
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=200)
sess = Session()
sess.init_app(app)
gk = GateKeeper(app, ban_rule={"count":5,"window":3,"duration":60}, rate_limit_rules=[ {"count":4,"window":1, "duration":120}, {"count":15,"window":7,"duration":240}])

from website.views import views
from website.auth import auth
from website.navfix import navfix
from website.users_pages import users_pages
from website.casino import casino
app.register_blueprint(users_pages, url_prefix='/')
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
app.register_blueprint(navfix, url_prefix='/')
app.register_blueprint(casino, url_prefix='/')
