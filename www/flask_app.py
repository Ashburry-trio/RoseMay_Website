#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations

from flask import Flask
from flask import render_template, redirect, request, session
from flask_session.__init__ import Session


app = Flask(__name__)
app.config['SERVER_NAME'] = "www.mslscript.com"
app.secret_key = "AadaDADSASDASDSDAasdsda1asdasd23423sdvbffbbfdbbnSDFDSFBfbs231"
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

from website.views import views
from website.auth import auth
app.register_blueprint(views, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')
