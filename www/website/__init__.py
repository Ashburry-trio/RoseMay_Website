#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import annotations

from flask import session, redirect, flash, make_response, render_template, request, url_for
from better_profanity import profanity
from fnmatch import fnmatch
from time import time as secstime
from shutil import copytree
from shutil import rmtree
from os import path, rename, rmdir, walk
from os.path import isdir, isfile
from configparser import ConfigParser
from chardet import detect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired

_dir = path.dirname(path.abspath(__file__))
app_dir = path.join(_dir, '..','app')


casino_user: ConfigParser[str,str] = ConfigParser()
casino_file = path.join(path.expanduser("~"), "www", "app", "casino.ini")
casino_app: ConfigParser[str,str] = ConfigParser()
casino_last_update: list[int] = [0]
email_file = path.join(path.expanduser("~"), "website_and_proxy", "email.ini")
user_dir: list[str | None] = [None]
user_file: list[str | None] = [None]

class xSearchForm(FlaskForm):
    search = StringField('XDCC Search',
                         render_kw={"class": "form-control me-2", "placeholder": "XDCC Search", "aria-label": "Search"},
                         validators=[DataRequired()])
    search_button = SubmitField('Search', render_kw={"class": "btn btn-outline-success", "type": "submit"})


def usable_decode(text: bytes | str) -> str:
    """Decode the bytes so it can be used.
        vars:
            :@param text: a bytes-string that needs decoding
            :@returns: the string of decoded bytes (str)
            :rtype: str
    """
    try:
        text = text.strip()
        if text == b'':
            return ''
        if type(text) == str:
            return text
        decoded_text: str = text.decode("latin1")
    except (UnicodeWarning, EncodingWarning, UnicodeDecodeError, UnicodeError, UnicodeTranslateError):
        try:
            decoded_text = text.decode("utf-8")
        except (UnicodeWarning, EncodingWarning, UnicodeDecodeError, UnicodeError, UnicodeTranslateError):
            # detect encoding:
            det: dict[str, str | float] = detect(text)
            return text.decode(det['encoding'], errors="replace")
    return decoded_text

# formerly def checkAlnum()
def validate_email_or_login(word: str, email: bool = False) -> [str,bool]:
    if ':' in word:
        passwd: str = word.split(':')[1]
        if passwd == 'nopass':
            word = word.split(':')[0] + ':nopass123'
        if passwd == 'nopass123':
            return False
        del passwd
    passwd: str
    login: str
    client_name: str
    word = colourstrip(word.strip())
    word = word.strip()
    word_len: int = len(word)
    word = word.lower()
    word = word.split()[0]
    word = word.strip(' @.:\x0c\f\n\t')
    word = word.strip()
    if (word_len > len(word)) or (' ' in word):
        return False
    username: str
    hostname: str = ''
    if email is True:
        if fnmatch(word,"*???@???*.?*"):
            username = word.split('@')[0].strip()
            hostname = word.split('@')[1].strip()
        else:
            return False
        word = username + '@' + hostname
        if profanity.contains_profanity(username) \
              or profanity.contains_profanity(hostname) \
              or username.startswith('.') \
              or username.startswith('-') or hostname[-1] in '_-.' \
              or hostname[0] in '_-.':
            return False
        if (fnmatch(word,'???*@???*.?*') is False) \
                or (len(word) > 63 or len(word) < 9) or (len(username) > 20 \
                or len(username) < 3) or (len(hostname) > 32 \
                or len(hostname) < 5) \
                or (word.count('@') != 1 or hostname.count('.') == 0) \
                or ':' in word or '..' in word or '--' in hostname \
                or '__' in word or '-_' in hostname or '_-' in hostname:
            return False
        if len(hostname) > 33 or hostname.startswith('.') \
              or hostname[-1] in '_-.' \
              or hostname[0] in '_-.' or ':' in hostname:
            return False

    elif not email:
        if fnmatch(word,'???*:????????*') and word.count(':') == 1:
            if fnmatch(word,'*@*') and word.count('@') == 1:
                client_name = word.split('@')[1]
                if not client_name.isalnum() or len(client_name) > 20 \
                      or len(client_name) < 2 \
                      or profanity.contains_profanity(client_name):
                    return False
                login = word.split('@')[0]
            else:
                login = word
        else:
            return False

        username = login.split(':')[0]
        passwd = login.split(':')[1]
        del login
        if len(username) > 30 or len(username) < 3:
            return False
        if len(passwd) > 32 or len(passwd) < 8:
            return False
        if '1' in username or '0' in username:
                return False
        if not passwd or passwd.startswith('javascript') \
          or passwd.startswith('return') or passwd.startswith('style') \
          or passwd.startswith('script') or '.' in passwd \
          or passwd.startswith('input') or passwd == 'pass' \
          or ':' in passwd or '@' in passwd:
            return False

    if not username or username.startswith('javascript') \
       or username.startswith('return') or username.startswith('style') \
       or username.startswith('script') or '.' in username \
       or username.startswith('input') or ':' in username \
       or '@' in username or 'admin' in username \
       or 'adm1n' in username or 'admln' in username \
       or profanity.contains_profanity(username):
        return False
    for L in word:
        if L.isalnum() or L == '_' or L == '-' or L == '.' or L == '@' or L == ':':
            continue
        return False
    return word


def clear_session():
    [session.pop(key) for key in list(session.keys()) if not key.startswith('_')]


def colourstrip(data_in: str | bytes) -> str:
    """Strips the mIRC colour codes from the text in variable data
        vars:
            :@param data: A string or bytes that might contains mSL colour codes
            :@returns: string without colour codes
            :rtype: str
    """
    data: str = usable_decode(data_in)
    del data_in
    data = data.strip()
    find = data.find("\x03")
    while find > -1:
        done = False
        data = data[:find] + data[find + 1:]
        if len(data) <= find:
            done = True
        try:
            if done:
                break
            if not int(data[find]) > -1:
                raise ValueError("Not-an-Number")
            data = data[:find] + data[find + 1:]
            try:
                if not int(data[find]) > -1:
                    raise ValueError("Not-an-Number")
            except IndexError:
                break
            except ValueError:
                data = data[:find] + data[find + 1:]
                continue
            data = data[:find] + data[find + 1:]
        except (ValueError, IndexError):
            if not done:
                if data[find] != ",":
                    done = True
        if (not done) and (len(data) >= find + 1) and (data[find] == ","):
            try:
                data = data[:find] + data[find + 1:]
                if not int(data[find]) > -1:
                    raise ValueError("Not-an-Number")
                data = data[:find] + data[find + 1:]
                if not int(data[find]) > -1:
                    raise ValueError("Not-an-Number")
                data = data[:find] + data[find + 1:]
            except ValueError:
                pass
            except IndexError:
                break
        find = data.find("\x03")
    data = data.replace("\x02", "")
    data = data.replace("\x1d", "")
    data = data.replace("\x1f", "")
    data = data.replace("\x16", "")
    data = data.replace("\x0f", "")
    data = data.replace("\x1e", "")
    return data


class NoSuchUser(BaseException):
    pass

def writePassword(secret: str, users: ConfigParser) -> None:
    users['passcode']['secret'] = secret
    try:
        save_user(users)
    except NoSuchUser:
        pass
    return None

def checkPassword(secret,users) -> bool:
    if not secret:
        return False
    if users.has_section('passcode') and 'secret' in users['passcode'].keys():
        if users['passcode']['secret'] == secret:
            return True
        else:
            return False
    else:
        raise NoSuchUser('website.checkPassword: User does not exist.')



def user_page_exists(username: str) -> bool:
    user_low: str = username.lower().strip()
    user_verify = validate_email_or_login(username.lower() + ':' + 'nopass')
    if not user_verify:
        return False
    if isdir(path.join(path.expanduser('~'), 'www', 'website', 'templates', 'users', user_low)):
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


def set_paths(username: str) -> bool:
    username_low: str = username.lower()
    del username
    user_dir[0] = ''
    user_file[0] = ''
    if not username_low:
        return False
    user_dir[0] = path.join(path.expanduser("~"), "website_and_proxy", "users", username_low)
    user_file[0] = path.join(path.expanduser("~"), "website_and_proxy", "users", username_low, username_low + ".ini")
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
    users: ConfigParser = ConfigParser()
    if username == None:
        if 'username' in session.keys():
            username = session['username']
        else:
            raise NoSuchUser('No username provided')
    username_low = username.lower()
    username_check: str | bool = username + ':nopass'
    username_check = validate_email_or_login(username_check)
    if username_check is False:
        raise NoSuchUser('Invalid username')

    if set_paths(username_low):
        try:
            users.read(user_file[0])
            if not users.has_section('passcode'):
                raise NoSuchUser
        except (FileNotFoundError, KeyError, ValueError) as e:
            raise NoSuchUser(str(e.args))
    return users

def fetch_user_by_detail(detail) -> [bool | str, bool | str, [bool | str, bool | str], [bool | str, bool | str]]:
    detail = detail.lower()
    if ':' in detail:
        e = False
        u = False
    elif '@' in detail:
        e = True
        u = False
    else:
        u = True
        e = False
        detail = detail + ':nopass'
    if e or u:
        if validate_email_or_login(word = detail, email = e) is False:
            return [False, False, [False, False], [False, False]]
        elif u:
            try:
                users = load_users_ini(detail)
                return [users['main']['username'], users['main']['email'], [users['main']['q1_q'], users['main']['q1_a']], [users['main']['q2_q'], users['main']['q2_a']]]

            except NoSuchUser:
                return [False, False, [False, False], [False, False]]
        else:
            try:
                users = load_users_email(username = None, email = detail)
                return [users['main']['username'], users['main']['email'], [users['main']['q1_q'], users['main']['q1_a']], [users['main']['q2_q'], users['main']['q2_a']]]

            except NoSuchUser:
                return [False, False, [False, False], [False, False]]
    else:
        try:
            users = load_users_ini(detail.split(':')[0])
            return [users['main']['username'], users['main']['email'], [users['main']['q1_q'], users['main']['q1_a']], [users['main']['q2_q'], users['main']['q2_a']]]
        except NoSuchUser:
            return [False, False, [False, False], [False, False]]


def load_users_email(username: str | None = None, email: str | None = None) -> [ConfigParser,bool]:
    global email_file
    users: ConfigParser = ConfigParser()
    if email is None:
        if 'username' in session.keys():
            username = session['username']
        try:
            if username:
                users = load_users_ini(username.lower())    # raises NoSuchUser
            else:
                raise NoSuchUser
        except NoSuchUser:
            raise
        email = users['main']['email']
    if not email:
        raise NoSuchUser
    users.read(email_file)
    username = users['email'][email]
    if not username:
        raise NoSuchUser
    return load_users_ini(username)

def login_user_post(username: str, password: str):
    users: ConfigParser
    clear_session()
    xsearch = xSearchForm()
    try:
        session['logged_in'] = False
        user_pass = username + ':' + password
        if not validate_email_or_login(user_pass, email = False):
            flash("Not a valid UserName or Password.", category="error")
            return make_response(render_template('login.html', xsearch=xsearch), 401)
        username_low: str = username.lower()
        del user_pass, username
        users = load_users_ini(username_low)    # Sets Paths (user_dir[0], user_file[0])
        if checkPassword(password,users):
            session['logged_in'] = True
            user_up: str = str(users['main']['username'])
            session['username'] = user_up
            session['power'] = str(users['main']['power']).lower() or 'normal'
            flash("You have logged-in successfully.", category='success')
            return redirect('/irc/proxies.html', code='307')
        else:
            flash("Bad Password for UserName.", category='error')
            return make_response(render_template('login.html', xsearch=xsearch), 401)
    except (ValueError, KeyError, FileNotFoundError, NoSuchUser) as exp:
        flash("Unknown UserName.", category="error")
        return make_response(render_template("login.html", xsearch=xsearch), 401)


def register_user_post(username: str, passwd: str, email: str, q1_q: str, q1_a: str, q2_q: str, q2_a: str, power: str = 'normal'):
    clear_session()
    users: ConfigParser
    q1_q = q1_q.strip()
    q1_a = q1_a.strip()
    q2_q = q2_q.strip()
    q2_a = q2_a.strip()
    xsearch = xSearchForm()
    username = username.strip(' \n\x03\t\f')
    passwd = passwd.strip(' \n\x03\t\f')
    session['logged_in'] = False
    password = passwd
    user_pass: str | bool = username + ':' + passwd
    user_pass = validate_email_or_login(user_pass)
    if False is user_pass:
        flash("Username must be <u><a href='https://simple.wikipedia.org/wiki/Alphanumeric' target='alphanumeric'>alphanumeric</a></u> <b>without</b> <a href='banned.html'>banned words</a>.", category='error')
        return make_response(render_template('register.html', xsearch=xsearch), 401)
    del user_pass
    username_low: str = username.lower()
    try:
        users = load_users_ini(username_low)
        if checkPassword(password,users) is True:
            users['main']['username'] = username
            if q1_q:
                users['main']['q1_q'] = q1_q.strip()
            if q1_a:
                users['main']['q1_a'] = q1_a.strip()
            if q2_q:
                users['main']['q2_q'] = q2_q.strip()
            if q2_a:
                users['main']['q2_a'] = q2_a.strip()
            # User already exists and they know the password
            session['username'] = user_up
            session['power'] = power.lower()
            session['logged_in'] = True
            users['main']['username'] = username
            user_up: str = users["main"]["username"]
            users['passcode']['secret'] = password
            writePassword(password, users)
            flash("You have logged-in successfully.", category='success')
            del user_up
            return redirect(url_for('auth.irc_proxies'), code='307')
        elif users.has_section('main'):
            flash('UserName is taken, bad Password. Try a different one.', category='error')
            clear_session()
            return make_response(render_template('register.html', xsearch=xsearch), 401)
        else:
            raise NoSuchUser

    except NoSuchUser:
        if not username_low:
            flash("You are missing the UserName to create.", category='error')
        elif 'admin' in username_low:
            flash("UserName MUST NOT contain the word 'Admin'.", category='error')
        elif username_low  == 'username':
            flash("Bad choice of UserName!", category='error')
        elif not password:
            flash("You MUST enter a Password you can remember.", category='error')
        elif len(password) < 8:
            flash('Password must be at-least 8 characters.', category='error')
        elif len(password) > 25:
            flash('Password must be, at-most, 25 characters.', category='error')
        else:
            src_dir = path.join(path.expanduser("~"), "website_and_proxy", "default_user")
            dst_dir = path.join(path.expanduser("~"), "website_and_proxy","users", username_low)
            try:
                copytree(src_dir, dst_dir)
                rename(path.join(dst_dir, 'default_user.ini'),path.join(dst_dir,username_low + '.ini'))
                users = load_users_ini(username_low)
                if q1_q:
                    users['main']['q1_q'] = q1_q.strip()
                if q1_a:
                    users['main']['q1_a'] = q1_a.strip()
                if q2_q:
                    users['main']['q2_q'] = q2_q.strip()
                if q2_a:
                    users['main']['q2_a'] = q2_a.strip()
                users['main']['power'] = power.lower()
                session["username"] = username
                session['logged_in'] = True
                users['main']['username'] = username
                writePassword(password,users)  # includes save_user()
                return redirect('/irc/proxies.html', code=307)
            except (FileExistsError) as e:
                flash('UserName already taken.', category='error')
    return make_response(render_template('register.html', xsearc=xsearch), 401)


custom_badwords = ['fuskk','fukkk','sexx','sexxx','loli','l0li','l@li',
    'penis','p3n1s','p3nls','p3nis','fukyou','fuckyou','fucku','l4li'
    'fukkyou','fukku','fukkku','fukkkyou','fukkme','fukkkme','fukkkm3',
    'fuckme','fuckm3','fukm3','fukkm3','kkk','focker','f0cker','f@cker',
    'fukkker','fukkk3r','f@kkk3r','f0kkker','suck dick','sukkk dick',
    'sukkk my dick','suck my dick','sukkk m3 dick','suk m3 dick','suk me d1ck',
    'suk m3 d1ck','suk m3 dlck','sukkk m3 dlck','suck m3 dlck','suky my dick',
    'suck my dickkk','nud3pics','nud3plcs','nudepics','nudeplcs','nudep1cs',
    'nud3pic','nud3plc','nud3p1c','nudepic','newdpics','n3wdpics','n3wdplc',
    'n3wdp1c','newdplc','newdp1c','newdpic', 'n3wd pics', 'newd pics',
    'newd p1cs','n3wd p1cs','newd plcs','n3wd plcs','n3wd pic', 'n3wd plc',
    'n3wd p1c', 'nude pic','nud3 pic', 'nude p1c','nude plc','nude pics',
    'nud3 pics', 'nud3 plcs','nud3 p1cs','lolicandy','l0licandy','l@licandy',
    'lolic4ndy','l0lic4ndy','l@lic4ndy','nudeme','nudeself','nud3',
    'k1ukkks','kkk1uks','k1ux','k1uxk','kluks','nud3s3lf','nud3self', 'ccunt',
    'kunt','kkunt','klukkks','klux','kkk','lolic@ndy','l0lic@ndy',
    'sucky my dick', 'your dick', 'ur dick', 'ur a dick', 'ura dick',
    'your a dick', 'u a dick', 'ua dick', 'uri dick', 'ur i dick','white power',
    'nigger','niggers','n1gger','n1ggers','nlgger','nlggers','black power',
    'white supremecy','white superemecy','white supremacy','white superemacy']

profanity.add_censor_words(custom_badwords)

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


def save_user(users) -> None:
    try:
        user = users['main']['username'] + ':nopass'
        username = validate_email_or_login(user, email = False)
        if not username:
            return NoSuchUser
        if not users.has_section('main'):
            raise NoSuchUser
        username = users['main']['username']
        for opt, val in session.items():
            opt = str(opt).lower()
            val = str(val)
            if opt and val and not opt.startswith('_'):
                users['main'][opt] = val
        with open(user_file[0], 'w') as fp:
            users.write(fp, space_around_delimiters = True)
    except (KeyError, ValueError, FileNotFoundError, NoSuchUser):
        clear_session()
        users.clear()
        return None
    if 'logged_in' in session:
        logged = bool(session['logged_in'])
    else:
        logged = False
    if 'power' in session:
        power = session['power'].lower()
    else:
        power = 'normal'
    clear_session()
    session['logged_in'] = logged
    if logged is True:
        session['username'] = username
        session['power'] = power

