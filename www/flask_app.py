#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations

from datetime import timedelta
from flask import Flask
from flask_session.__init__ import Session
from flask_argon2 import Argon2
from argon2 import Type
from argon2 import Parameters

LOW_MEMORY = Parameters(
    type=Type.ID,
    version=19,
    salt_len=8,
    hash_len=16,
    time_cost=3,
    memory_cost=50000,
    parallelism=1,
)

app = Flask(__name__)
key: str
with open("/home/Ashburry/secret.txt", 'r') as fp:
    key = fp.read()
key = key.strip()
app.config['SERVER_NAME'] = "www.mslscript.com"
app.secret_key = key or "asdf2348adhf234jkhsdf87234jbsvdh1234h2h3jkk5"
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config['SESSION_FILE_THRESHOLD'] = 250
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=10)
Session(app)
app.config['TIME_COST'] = 3
app.config['SALT_LEN'] = 8
app.config['HASH_LEN'] = 16
app.config['MEMORY_COST'] = 50000
app.config['PARALLELISM'] = 1
crypt_app = Argon2(app)



from website.views import views
from website.auth import auth

app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
from website.casino import casino
app.register_blueprint(casino, url_prefix='/')

