#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import annotations
from flask import Blueprint, render_template, request, flash
# from werkzeug.security import generate_password_hash, check_password_hash
from flask import redirect, session
auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')
from . import login_user_post, register_user_post, save_user, load_users_ini


@auth.route("/irc/proxies.html", methods=["POST", "GET"])
@auth.route("/proxy.html", methods=["POST", "GET"])
@auth.route("/proxies.html", methods=["POST", "GET"])
def irc_proxies():
    if 'logged_in' in session:
        if session['logged_in'] == 'True':
            proxy_list: dict[str | None, str | None]
            users = load_users_ini(session['username'].lower())
            if 'proxy' in users.keys():
                proxy_list = users['proxy']
            else:
                proxy_list = {}
            return render_template('proxies.html', bnc_list=proxy_list)
        else:
            flash("Logged_in = False", category='error')
            return redirect('/login.html')
    flash("Logged_in = None", category='error')
    return redirect('/login.html')


@auth.route("/login", methods=["POST", "GET"])
@auth.route("/login.html", methods=["POST", "GET"])
def login():
    session['logged_in'] = 'False'
    if request.method == "POST":
        # record the user name
        username = request.form.get("username")
        passw = request.form.get("password")
        if not passw: passw = ''
        if not username: username = ''
        username = username.strip()
        passw = passw.strip()
        if not passw or not username:
            flash('Password/UserName fields are blank?', category='error')
        else:
            return login_user_post(username, passw)
    return render_template("login.html")


@auth.route('/logout')
@auth.route('/logout.html')
def logout():
    session['logged_in'] = 'False'
    save_user()
    flash("You have logged-out successfully!", category='success')
    return redirect('/index.html')


@auth.route('/register', methods=['GET', 'POST'])
@auth.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        session['logged_in'] = 'False'
        username: str = request.form.get('username')
        pass1: str = request.form.get('password1')
        pass2: str = request.form.get('password2')
        return register_user_post(username, pass1, pass2)
    return render_template("register.html")
