#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import annotations

from flask import session, redirect, flash, make_response, render_template
from time import time as timesecs
from shutil import copytree
from configparser import ConfigParser
from os import path, rename
from os.path import isdir
import flask_argon2

_dir = path.dirname(path.abspath(__file__))
app_dir = path.join(_dir, '../app')

users: ConfigParser[str | None, str | None, str | None] = ConfigParser()
casino_user: ConfigParser[str | None, str | None, str | None] = ConfigParser()
casino_file: str = path.join(path.expanduser("~"), "www", "app", "casino.ini")
casino_app: ConfigParser = ConfigParser()
casino_last_update: list[int] = [0]

user_dir: list[str | None] = [None]
user_file: list[str | None] = [None]

def checkAlnum(word: str):
    if not word:
        return False
    for L in word:
        if L.isdigit() or L.isalpha():
            continue
        return False
    return True

def clear_session():
    [session.pop(key) for key in list(session.keys()) if not key.startswith('_')]


class BadHash(BaseException):
    pass


class NoSuchUser(BaseException):
    pass

def gph(secret: str):
    try:
        return flask_argon2.generate_password_hash(secret)
    except BaseException:
        raise BadHash

def checkPassword(hash, secret):
    try:
        verify = flask_argon2.check_password_hash(hash, secret)
    except BaseException:
        raise BadHash
    return verify

def strip_code(m):
    return strip_html(m)

def strip_html(msg):
    """
      Takes in 'msg' with py and html and path codes and
      removes the nasty bytes. Decodes bytes to string.
      Returns (msg, bool) boolean is True if 'msg' is modified or blank.
    """
    if not msg:
        return ('', True)
    if isinstance(msg, bytes):
        try:
            msg = msg.decode('utf-8', errors='replace')
        except (UnicodeWarning, UnicodeDecodeError, UnicodeError, UnicodeTranslateError):
            return ('', True)

    length = len(msg)
    msg = msg.replace('\n','')
    msg = msg.replace('\r','')
    msg = msg.replace('\f','')
    msg = msg.replace('\t','')
    msg = msg.replace('<','')
    msg = msg.replace('>','')
    msg = msg.replace('&','')
    msg = msg.replace('?','')
    msg = msg.replace('=','')
    msg = msg.replace('+','')
    msg = msg.replace(' ','')
    msg = msg.replace('"','')
    msg = msg.replace("'",'')
    msg = msg.replace('`','')
    msg = msg.replace('\\','')
    msg = msg.replace('/','')
    msg = msg.replace('{','')
    msg = msg.replace('}','')
    msg = msg.replace('.','')
    msg = msg.replace(':','')
    msg = msg.replace(';','')
    msg = msg.replace('@','')
    msg = msg.replace('~','')
    if checkAlnum(msg) == False:
        return (msg, True)
    if len(msg) < length:
        return (msg, True)
    return (msg, False)


def user_exists(user: str):
    user_low: str = user.lower()
    del user
    user_low = strip_html(user_low)
    if user_low[1]:
        return False
    if isdir(path.join(path.expanduser('~'), 'website_and_proxy', 'users' + user_low[0])):
        return True
    return False


def set_paths(username: str):
    username_low: str = strip_html(username.lower())
    del username
    if username_low[1]:
        return
    user_dir[0] = path.join(path.expanduser("~"), "website_and_proxy", "users", username_low[0])
    user_file[0] = path.join(path.expanduser("~"), "website_and_proxy", "users", username_low[0], username_low[0] + ".ini")

def load_casino_user(username: str | None = None):
    username_low: tuple[str, bool]
    if username:
        username_low = strip_html(username.lower())
    else:
        if 'username' in session.keys():
            username = session['username']
            username_low = strip_html(username.lower())
        else:
            return False
    del username
    casino_file_name = path.join(path.expanduser("~"), "website_and_proxy", "users", f"{username_low[0]}", "casino.ini")
    casino_user.read(casino_file_name)
    return casino_user


def load_casino_app():
    casino_app.read(casino_file)
    return casino_app

def save_casino_app():
    with open(casino_file, 'w') as fp:
        casino_app.write(fp, space_around_delimiters=True)
    casino_last_update[0] = int(timesecs())

def load_users_ini(username: str | None = None):
    if not username:
        if 'username' in session.keys():
            username = session['username']
        else:
            return False
    username_low: str = strip_html(username.lower())
    del username
    if username_low[1]:
        raise ValueError('Not a valid UserName.')
    set_paths(username_low[0])
    users.read(user_file[0])
    return users


# def load_default_user():
#    users.read(path.expanduser("~/website_and_proxy/default_user/default_user.ini"))
#    return users


def login_user_post(username: str, password: str):
    try:
        username = strip_html(username)
        password = strip_html(password)
        if username[1] or password[1]:
            flash("Not a valid UserName or Password.")
            return redirect('/login.html')
        username_low: str = username[0].lower()
        load_users_ini(username_low)
        session['logged_in'] = 'False'
        try:
            ph_hash = checkPassword(users['main']['password'], password[0])
        except BadHash:
            flash('error checking password. try again...')
            return make_response(redirect('/login.html'), 401)
        if ph_hash:
            session['logged_in'] = 'True'
            session['username'] = str(users['main']['username'])
            session['password'] = str(users['main']['password'])
            session['power'] = str(users['main']['power']) or 'normal'
            save_user()
            flash(f'you have logged-in with {username[0]} : {password[0]}', category='success')
            return redirect('/irc/proxies.html')
        else:
            flash(f'bad password! {password[0]}', category='error')
            return make_response(render_template('login.html'), 401)
    except (ValueError, KeyError, FileNotFoundError):
        flash("unknown UserName.", category="error")
        return make_response(render_template("login.html"), 401)


def register_user_post(username: str, passwd: str, power = 'normal'):
    password: list[str, bool] = strip_html(passwd)
    username: list[str, bool] = strip_html(username)
    if username[1] or password[1]:
        if username[1]:
            flash('not a valid UserName, it must be alphabetic and digits only.')
        if password[1]:
            flash('Password MUST contain alphabetic and digit characters only.', category='error')
        return render_template('register.html')
    username_low: str = username[0].lower()
    clear_session()
    session['username'] = username[0]
    session['logged_in'] = 'False'
    users.clear()
    try:
        # User already exists and they know the password
        load_users_ini(username_low)
        if not users.has_section('main'):
            raise NoSuchUser
        try:
            ph_hash = checkPassword(users['main']['password'], password[0])
        except BadHash:
            flash('error checking password. try a different password.', category='error')
            return make_response(render_template('register.html'), 401)
        if ph_hash:
            session['password'] = users['main']['password']
            session['username'] = username[0]
            session['logged_in'] = 'True'
            save_user()
            flash(f"you just logged-in with {username[0]} : {password[0]}", category='success')
            return make_response(redirect('/irc/proxies.html'), 307)
        else:
            flash('UserName is taken, try again or try to log-in...', category='error')
            clear_session()
            session['logged_in'] = 'False'
            return render_template('register.html')
    except (KeyError, ValueError, FileNotFoundError, NoSuchUser):
        if not username_low:
            flash("i am missing the UserName to create.", category='error')
        elif 'admin' in username_low:
            flash("UserName MUST NOT contain the word 'Admin'.", category='error')
        elif username_low  == 'username':
            flash("bad choice of UserName!", category='error')
        elif len(username_low) < 5 or len(username_low) > 15:
            flash("UserName MUST NOT have more than 15 nor less-than 5 characters.", category="error")
            return make_template('register.html')
        elif not password[0]:
            flash("you MUST enter a Password you can remember.", category='error')
        elif len(password[0]) < 5:
            flash('Password must be at-least 5 characters.', category='error')
        elif len(password[0]) > 15:
            flash('Password must be, at-most, 15 characters.', category='error')
        else:
            try:
                session["username"] = username[0]
                try:
                    password_secret = gph(password[0])
                except BadHash:
                    flash("invalid Password.", category='error')
                    return make_response(render_template('register.html'), 401)
                session['logged_in'] = 'True'
                session['power'] = power
                src_dir = path.join(path.expanduser("~"), "website_and_proxy", "default_user")
                src_file = path.join(path.expanduser("~"), "website_and_proxy", "users", f"{username_low}", 'default_user.ini')
                set_paths(username_low)
                copytree(src_dir, user_dir[0])
                rename(src_file, user_file[0])
                load_users_ini(username_low)
                session['password'] = password_secret
                save_user()
                flash(f"UserName {username[0]} was created with password {password[0]}...")
                return make_response(redirect('/irc/proxies.html'), 307)
            except (FileExistsError,):
                pass
        clear_session()
        session['logged_in'] = 'False'
        return make_response(render_template('register.html'), 401)


def save_casino_user(username: str | None = None) -> None:
    if not casino_user:
        return None
    if not casino_user.has_section('main'):
        return None
    if not username:
        username = session['username']
    if not username:
        return None
    username_low: list[str, bool] = strip_html(username.lower())
    if username_low[1]:
        return None
    casio_file_name = path.join(path.expanduser("~"), "website_and_proxy", "users", f"{username_low[0]}", "casino.ini")
    with open(casino_file_name, 'w') as fp:
        fp.write(casino_user, space_around_delimiters=True)
    return None


def save_user() -> None:
    try:
        username = strip_html(session['username'])
        username_low: str = username[0].lower()
        if username[1]:
            return None
        set_paths(username_low)
        load_users_ini(username_low)
        if not users.has_section('main'):
            users['main'] = {}
        for opt, val in session.items():
            opt = str(opt)
            val = str(val)
            if opt and val and not opt.startswith('_'):
                opt = opt.lower()
                users['main'][opt] = val
        with open(user_file[0], 'w') as fp:
            users.write(fp, space_around_delimiters=True)
    except (KeyError, ValueError, FileNotFoundError):
        clear_session()
        users.clear()
        return
    logged = str(session['logged_in'])
    power = session['power']
    clear_session()
    session['logged_in'] = logged
    if logged == 'True':
        session['username'] = username[0]
        session['power'] = power
