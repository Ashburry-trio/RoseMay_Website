#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations

from datetime import timedelta
from flask import Flask
from flask import request
from flask_session import Session
from flask_gatekeeper import GateKeeper
from os.path import expanduser
app = Flask(__name__)
key: str
try:
    with open(expanduser("~/secret.txt"), 'r') as fp:
        key = fp.read()
except (NameError, FileNotFoundError):
    import random
    import string
    def random_string(length):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(length))
    with open(expanduser("~/secret.txt"), 'w') as fp:
        LETTERS = random_string(50)
        fp.write(LETTERS)
        key = LETTERS

key = key.strip()
app.config['SERVER_NAME'] = "www.mslscript.com"
app.secret_key = key or "Jsd2f3oasd4FDSEf;asdfjkajkdf12u3y908)(*@#$*(,.;"
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_FILE_DIR"] = expanduser('~/flask_session_cache')
app.config["SESSION_TYPE"] = "filesystem"
app.config['SESSION_FILE_THRESHOLD'] = 250
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=10)
gk = GateKeeper(app, ban_rule={"count":5,"window":3,"duration":60}, rate_limit_rules=[ {"count":4,"window":1, "duration":120}, {"count":15,"window":7,"duration":240}])
Session(app)

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
