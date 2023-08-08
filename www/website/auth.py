from flask import Blueprint, render_template

from flask import request, flash, redirect, url_for
#from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

import os
from . import login_user_post, register_user_post, save_user, load_users_ini

@auth.route("/proxies/", methods=["POST", "GET"])
@auth.route("/proxy/", methods=["POST", "GET"])
@auth.route("/irc/proxy.html", methods=["POST", "GET"])
@auth.route("/irc/proxies.html", methods=["POST", "GET"])
@auth.route("/proxy.html", methods=["POST", "GET"])
@auth.route("/proxies.html", methods=["POST", "GET"])
def irc_proxies():
    if 'logged_in' in session:
        if session['logged_in'] == 'True':
            proxy_list: dict[str | None, str | None]
            users = load_users_ini(session['username'])
            if not users.has_section('proxy'):
                users['proxy'] = {}
            proxy_list = users['proxy']
            return render_template('proxies.html', bnc_list=proxy_list, passcode=users['main']['password'])
    return render_template('proxy-login.html')


@auth.route("/login/", methods=["POST", "GET"])
@auth.route("/login.html", methods=["POST", "GET"])
def login():
    if 'logged_in' in session.keys() and session['logged_in'] == 'True':
        flash(f"Already logged-in with: {session['username']}", category='error')
        return redirect('/proxies.html')
    if request.method == "POST":
        # record the user name
        username = request.form.get("username")
        passw = request.form.get("password")
        username = username.strip()
        passw = passw.strip()
        if not passw: passw = ''
        if not username: username = ''
        if not username.isalpha() or not passw.isalpha():
            flash('You must use alphabetic characters only.', category='error')
        elif not passw or not username:
            flash('UserName or password fields are blank?', category='error')
        else:
            return login_user_post(username, passw)
    return render_template("login.html")



@auth.route('/logout/')
@auth.route('/logout.html')
def logout():
    if 'logged_in' in session.keys() and session['logged_in'] != 'True':
        flash("You ARE NOT logged-in.", category='error')
    else:
        flash("You have logged-out successfully!", category='success')
    session['logged_in'] = 'False'
    if 'username' in session.keys():
        save_user()
    return redirect('/index.html')


@auth.route('/register/', methods=['GET', 'POST'])
@auth.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        session['logged_in'] = 'False'
        username: str = request.form.get('username')
        pass1: str = request.form.get('password1')
        pass2: str = request.form.get('password2')
        if not username.isalpha() or not pass1.isalpha() or not pass2.isalpha():
            flash('You must use alphabetic characters only.', category='error')
        else:
            return register_user_post(username, pass1, pass2)
    return render_template("register.html")




