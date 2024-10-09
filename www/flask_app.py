#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations

from datetime import timedelta
from flask import Flask, request
from flask_session import Session
from flask_gatekeeper import GateKeeper
from os.path import expanduser
import os
import sys


mykey: str | bool | bytes

def init_mykey():
    global mykey
    mykey = make_key("style\=Secret-key-not-inuse-p1s-change-these-words-to-" \
                            + "random-Tex1")

def make_key(key2: str | bytes | bool = None):
    global mykey
    secret_file: str = expanduser(os.path.join("~",'secret.txt'))
    try:
        if mykey and not key2:
            key2 = mykey
        if not mykey and not key2:
            with open(secret_file, 'r') as fp:
                key2 = fp.read()
        from os import remove
        remove(secret_file)
    except (NameError, FileNotFoundError):
        import secrets
        with open(secret_file, 'w') as fp:
            LETTERS = secrets.token_urlsafe(190)
            fp.write(LETTERS)
            key2 = secrets.token_urlsafe(200)
        del secrets
        del LETTERS
    if bytes == type(key2):
        key2 = bytes.decode(key2, 'utf-8')
    key2 = str.strip(key2, ' \n\0x5\t\f')
    for single_char in key2:
        if not char_is_good(single_char):
            key2 = 'yourkey\"-was_not\'Alphanumeric/","-removeall-specialchars+'
            break
    key2 = bytes(key2[0:100], 'utf-8')
    del secret_file
    return key2

def char_is_good(single_char: str | bytes):
    if bytes == type(single_char):
        single_char = bytes.decode(single_char, 'utf-8')
    if not single_char.isalnum() and not single_char in ' _-,.<>/?;:\'\"' \
                    + '{}[]()+=!@#$\§%^&*\\|':
        return False
    return True

def test_key_len():
    global mykey
    from warnings import warn
    if len(mykey) < 90:
        warn("'Your Private Key is Less Than 90 Characters" \
                + " in Length, Secret can be 100 Characters.")

app = Flask(__name__)
init_mykey()
app.secret_key = mykey

app.config['SERVER_NAME'] = 'ashburry.pythonanywhere.com'
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_FILE_DIR"] = expanduser(os.path.join('~','flask_session_cache'))
app.config["SESSION_TYPE"] = "filesystem"     #  or file
app.config['SESSION_FILE_THRESHOLD'] = 250
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=200)
sess = Session()
sess.init_app(app)
gk = GateKeeper(app, ban_rule={"count":15, "window":3, "duration":60}, \
        rate_limit_rules=[{"count":20, "window":10, "duration":45}, \
                        {"count":15, "window":7, "duration":35}])

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
