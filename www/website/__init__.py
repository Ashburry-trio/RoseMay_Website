#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import annotations

from flask import session, redirect, flash, make_response, render_template, request, url_for
from time import time as secstime
from shutil import copytree
from shutil import rmtree
from os import path, rename, rmdir, walk
from os.path import isdir, isfile
from configparser import ConfigParser

_dir = path.dirname(path.abspath(__file__))
app_dir = path.join(_dir, '..','app')

users: ConfigParser[str] = ConfigParser()
casino_user: ConfigParser[str] = ConfigParser()
casino_file = path.join(path.expanduser("~"), "www", "app", "casino.ini")
casino_app: ConfigParser[str] = ConfigParser()
casino_last_update: list[int] = [0]

user_dir: list[str | None] = [None]
user_file: list[str | None] = [None]

def checkAlnum(word: str. email = False) -> bool:
    word = word.lower()
    if email is True:
        if email.count('@') != 1 or email.count('.') != 1:
            return False
    if not word or 'javascript' in word or 'return' in word or 'style' in word or 'script' in word:
        return False
    for L in word:
        if L.isdigit() or L.isalpha() or L == '_' or L == '-' or ((L == '@' or L = '.') and email is True):
            continue
        return False
    return True

def clear_session():
    [session.pop(key) for key in list(session.keys()) if not key.startswith('_')]


class NoSuchUser(BaseException):
    pass

def writePassword(secret: str) -> None:
    users['passcode']['secret'] = secret
    save_user()
    return None

def checkPassword(secret) -> bool:
    if not secret:
        return False
    if users.has_section('passcode') and 'secret' in users['passcode'].keys():
        if users['passcode']['secret'] == secret:
            return True
        else:
            return False
    else:
        raise NoSuchUser('__init__.checkPassword: User does not exist.')

def strip_code(m: str) -> list:
    return strip_html(m)

def strip_html(msg: str, email = False) -> list:
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
    msg = msg.replace('%','')
    msg = msg.replace('!','')
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
    msg = msg.replace(':','')
    msg = msg.replace(';','')
    if email == False:
        msg = msg.replace('@','')
        msg = msg.replace('.','')
    msg = msg.replace('~','')
    if checkAlnum(msg, email) == False:
        return (msg, True)
    if len(msg) < length:
        return (msg, True)
    return (msg, False)

def user_page_exists(username: str) -> bool:
    user_strip: list[str, bool]
    user_strip = strip_html(username.lower())
    if user_strip[1]:
        return False
    if isdir(path.join(path.expanduser('~'), 'www', 'website', 'templates', 'users', user_strip[0])):
        return True
    else:
        return False

def get_user_pages():
    user_dirs = next(walk(path.expanduser(path.join('~','www','website','templates','users'))),(None,[],None))[1]
    total_nicklist = set()
    total_chanlist = set()
    for udir in user_dirs:
        nets = next(walk(path.expanduser(path.join('~','www','website','templates','users', udir))),(None,[],None))[1]
        for net in nets:
            nicklist = set()
            chanlist = set()
            ass_ini = path.expanduser(path.join('~','www','website','templates','users', udir, net, 'assets.ini'))
            config_ini = ConfigParser()
            config_ini.read(ass_ini)
            if 'nicks' in config_ini.keys() and 'nicks' in config_ini['nicks'].keys():
                for nick in config_ini['nicks']['nicks'].split(' '):
                    nicklist.add(nick)
            if 'chans' in config_ini.keys() and 'chans' in config_ini['chans'].keys():
                for chan in config_ini['chans']['chans'].split(' '):
                    chanlist.add(chan)
            total_nicklist.add((net, udir, tuple(nicklist)))
            total_chanlist.add((net, udir, tuple(chanlist)))
    asset_list: tuple[tuple[str, str, tuple[str] | None],tuple[str, str, tuple[str] | None]] = (sorted(tuple(total_chanlist)), sorted(tuple(total_nicklist)))
    return asset_list
    # asset_list[0] is Chan list
    # asset_list[1] is Nickname list


def user_exists(username: str) -> bool:
    user_low: str = username.lower()
    del username
    user_low_strip: list[str, bool] = strip_html(user_low)
    if user_low_strip[1]:
        return False
    if isdir(path.join(path.expanduser('~'), 'website_and_proxy', 'users', user_low_strip[0])):
        return True
    return False


def set_paths(username: str) -> None | bool:
    username_low: list[str, bool] = strip_html(username.lower())
    del username
    user_dir[0] = ''
    user_file[0] = ''
    if username_low[1]:
        return None
    user_dir[0] = path.join(path.expanduser("~"), "website_and_proxy", "users", username_low[0])
    user_file[0] = path.join(path.expanduser("~"), "website_and_proxy", "users", username_low[0], username_low[0] + ".ini")
    if isfile(user_file[0]):
        return True
    else:
        return False

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
    casino_last_update[0] = int(secstime())

def load_users_ini(username: str | None = None) -> ConfigParser | None:
    global users
    users.clear()
    if username == None:
        if 'username' in session.keys():
            username = session['username']
        else:
            return
    username_low: str = strip_html(username.lower())
    del username
    if set_paths(username_low[0]):
        users.read(user_file[0])
    return users

def fetch_user_by_detail(detail):
    detail = detail.lower()
    if '@' in detail:
        e = True
        detail_strip: list[str, bool] = strip_html(detail, email = True)
    else:
        e = False
        detail_strip: list[str, bool] = strip_html(detail)

    if detail_strip[1] is True or e:
        if detail_strip[1] is True:
            flash('Invalid UserName or Email address')
        if e:
            flash('Email lookup is not supported yet")
        return False, False, [False, False], [False, False]
    if user_exsits(detail):
        users = load_users_ini(detail)
        return detail, users['main']['email'], [users['main']['q1.q'], users['main']['q1.a']] , [users['main']['q2.q'], users['main']['q2.a']]
    else:
        return False, False, [False, False], [False, False]
# def load_default_user():
#    users.read(path.expanduser("~/website_and_proxy/default_user/default_user.ini"))
#    return users


def login_user_post(username: str, password: str):
    clear_session()
    try:
        session['logged_in'] = False
        user_strip: list[str, bool] = strip_html(username)
        pass_strip: list[str, bool] = strip_html(password)
        del username, password
        if user_strip[1] or pass_strip[1]:
            flash("Not a valid UserName or Password.")
            return make_response(render_template('login.html'), 401)
        username_low: str = str(user_strip[0]).lower()
        load_users_ini(username_low)    # Sets Paths (user_dir[0], user_file[0])
        if checkPassword(pass_strip[0]):
            session['logged_in'] = True
            user_up: str = str(users['main']['username'])
            session['username'] = str(users['main']['username']).lower()
            session['power'] = str(users['main']['power']) or 'normal'
            flash(f"You have logged-in as \'{user_up}\'", category='success')
            return redirect('/irc/proxies.html', code='307')
        else:
            flash(f"bad password! \'{pass_strip[0]}\'", category='error')
            return make_response(render_template('login.html'), 401)
    except (ValueError, KeyError, FileNotFoundError, NoSuchUser) as exp:
        flash(f"Unknown UserName.", category="error")
        return make_response(render_template("login.html"), 401)


def register_user_post(username: str, passwd: str, q1: list[str, str], q2: list[str, str], power = 'normal'):
    clear_session()
    global users
    users.clear()
    users['main'] = {}
    password_strip: list[str, bool] = strip_html(passwd)
    username_strip: list[str, bool] = strip_html(username)
    del passwd, username
    if username_strip[1] or password_strip[1]:
        if username_strip[1]:
            flash('Not a valid UserName, it must be alphabetic and digits only.', category='error')
        elif password_strip[1]:
            flash('Password MUST contain alphabetic and digits only.', category='error')
        return make_response(render_template('register.html'), 401)
    username_low: str = str(username_strip[0]).lower()
    try:
        load_users_ini(username_low)
        users['main']['username'] = username_strip[0]
        users['main']['q1'] = q1
        users['main']['q2'] = q2
        # User already exists and they know the password
        # load_users_ini(username_low)
        session['logged_in'] = False
        session['username'] = username_low
        if checkPassword(password_strip[0]) is True:
            user_up: str = users["main"]["username"]
            session['username'] = user_up.lower()
            session['power'] = users['main']['power']
            session['logged_in'] = True
            flash(f"You have logged-in as \'{user_up}\'", category='success')
            del user_up
            return redirect(url_for('auth.irc_proxies'), code='307')
        else:
            flash('UserName is taken. Try Again...', category='error')
            clear_session()
            session['logged_in'] = False
            del session['username']
            return make_response(render_template('register.html'), 401)
    except (KeyError, ValueError, FileNotFoundError, NoSuchUser):
        if not username_low:
            flash("You are missing the UserName to create.", category='error')
        elif 'admin' in username_low:
            flash("UserName MUST NOT contain the word 'Admin'.", category='error')
        elif username_low  == 'username':
            flash("bad choice of UserName!", category='error')
        elif not password_strip[0]:
            flash("you MUST enter a Password you can remember.", category='error')
        elif len(password_strip[0]) < 5:
            flash('Password must be at-least 5 characters.', category='error')
        elif len(password_strip[0]) > 15:
            flash('Password must be, at-most, 15 characters.', category='error')
        else:
            session["username"] = username_strip[0].lower()
            src_dir = path.join(path.expanduser("~"), "website_and_proxy", "default_user")
            src_file = path.join(path.expanduser("~"), "website_and_proxy", "users", f"{username_low}", 'default_user.ini')
            set_paths(username_low)
            try:
                copytree(src_dir, user_dir[0])
                rename(src_file, user_file[0])
                users = load_users_ini(username_low)
            except FileExistsError:
                pass
            session['username'] = username_strip[0].lower()

            users['main']['username'] = username_strip[0]
            session['power'] = power
            users['main']['q1.q'] = q1[0]
            users['main']['q1.a'] = q1[1]
            users['main']['q2.q'] = q2[0]
            users['main']['q2.a'] = q2[1]
            session['logged_in'] = True
            writePassword(password_strip[0])  # includes save_user()
            flash(f"UserName \'{username_strip[0]}\' was just created and saved...")
            return redirect('/irc/proxies.html', code='307')
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
        username = strip_html(users['main']['username'])
        if username[1]:
            return None
        if not users.has_section('main'):
            raise NoSuchUser
        for opt, val in session.items():
            opt = str(opt).lower()
            val = str(val)
            if opt and val and not opt.startswith('_') and opt != 'secret' and opt != 'username':
                users['main'][opt] = val
        with open(user_file[0], 'w') as fp:
            users.write(fp, space_around_delimiters=True)
    except (KeyError, ValueError, FileNotFoundError, NoSuchUser):
        clear_session()
        users.clear()
        return None
    logged = bool(session['logged_in'])
    power = session['power']
    clear_session()
    session['logged_in'] = logged
    if logged is True:
        session['username'] = username[0].lower()
        session['power'] = power
