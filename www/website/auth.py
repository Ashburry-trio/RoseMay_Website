from flask import Blueprint, render_template, make_response
from flask import request, flash, redirect
#from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from flask_app import gk, limiter
from os.path import expanduser
from os import path
from time import time as ctime
import os
from configparser import ConfigParser
import hashlib
from website.ipreg import get_ip_info
from website import login_user_post, register_user_post, save_user, load_users_ini, validate_email_or_login, fetch_user_by_detail
from website import xSearchForm
auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

@auth.route("/irc/script.html", methods=["POST", "GET"])
@auth.route("/irc/scripts.html", methods=["POST", "GET"])
@auth.route("/script/", methods=["POST", "GET"])
@auth.route("/scripts/", methods=["POST", "GET"])
@auth.route("/script.html", methods=["POST", "GET"])
@auth.route("/scripts.html", methods=["POST", "GET"])
def proxy_scripts():
    gk.report()
    xsearch = xSearchForm()
    if 'logged_in' in session.keys() and session['logged_in'] is True:
            return render_template(path.join('scripts', 'scripts.html'), xsearch=xsearch)
    else:
        return make_response(render_template(path.join('scripts', 'no-scripts.html'), xsearch=xsearch), 401)


@auth.route("/proxies/", methods=["POST", "GET"])
@auth.route("/proxy/", methods=["POST", "GET"])
@auth.route("/irc/proxy.html", methods=["POST", "GET"])
@auth.route("/irc/proxies.html", methods=["POST", "GET"])
@auth.route("/proxy.html", methods=["POST", "GET"])
@auth.route("/proxies.html", methods=["POST", "GET"])
def irc_proxies():
    gk.report()
    xsearch = xSearchForm()
    if 'logged_in' in session.keys() and session['logged_in'] is True:
        proxy_list: dict[str, str]
        users = load_users_ini(session['username'])
        # nothing here
        if users.has_section('proxy'):
            proxy_list = users['proxy']
        else:
            proxy_list = dict()
            proxy_list['proxy'] = {}
            proxy_list['proxy']['0.0.0.1'] = 'soem,thi9ng new'
            users = dict()
            users['passcode'] = {}
            users['passcode']['secret'] = 'hell_no-This_does_not_work'
        return render_template('proxies.html', bnc_list=proxy_list, passcode=users['passcode']['secret'], xsearch=xsearch)
    else:
        return render_template('proxy-login.html', xsearch=xsearch)

@auth.route("/login/", methods=["POST", "GET"])
@auth.route("/login.html", methods=["POST", "GET"])
@limiter.limit("13 per minute")
def login():
    gk.report()
    xsearch = xSearchForm()
    try:
        pass
#        client_ip: str = get_ip_checked(request)
    except Exception:
        session['logged_in'] = False
        return redirect('/index.html', code=307)
    session['logged_in'] = False
    if request.method == "POST":
        # record the user name
        username: str = request.form.get("username", '')
        passwd: str = request.form.get("password", '')
        username = username.strip(' \n\0x5\t\f')
        passwd = passwd.strip(' \n\0x5\t\f')
        user_pass = username + ':' + passwd
        user_pass = validate_email_or_login(user_pass, email = False)
        if not user_pass:
            flash('UserName and/or Password field is NOT valid.', category='error')
        else:
            # Put xsearch in below
            return login_user_post(username, passwd)
    return make_response(render_template("login.html", content_page_name='login', xsearch=xsearch), 401)



@auth.route('/logout/', methods=['GET'])
@auth.route('/logout.html', methods=['GET'])
def logout():
    gk.report()
    if ('logged_in' in session.keys() and session['logged_in'] is not True) or 'logged_in' not in session.keys():
        flash("You ARE NOT logged-in.", category='error')
    else:
        flash("You have signed-out successfully!", category='success')
    session['logged_in'] = False
    return redirect('/index.html', code='307')

def delete_file(file_path: str) -> bool:
    try:
        os.remove(file_path)
    except FileNotFoundError:
        return True
    except Exception:
        return False
    return True

import json

def dict_to_configparser(data_dict):
    config = ConfigParser()
    config['DEFAULT'] = {}
    try:
        for section, options in data_dict.items():
            if type(options) is dict:
                config.add_section(section)
                for key, value in options.items():
                    if type(value) is dict:
                        config.add_section(f"{section}.{key}")
                        for sect,val in value.items():
                            if type(val) is dict:
                                config.add_section(f"{section}.{key}.{sect}")
                                for sect3,val3 in val.items():
                                    config.set(f"{section}.{key}.{sect}", str(sect3), str(val3))
                            else:
                                config.set(f"{section}.{key}", str(sect), str(val))
                    else:
                        config.set(section, key, str(value))  # Ensure value is a string
            elif options is None:
                config.set('DEFAULT', section, 'None')
            elif type(options) is str or type(options) is bool:
                config.set('DEFAULT',section,str(options))
            else:
                config.add_section('dummy')
                config['dummy']['key.for'] = 'section: '+str(section)+' options_type: '+str(type(options))
    except Exception:
        config['dummy']['key.except'] = str(data_dict)
    finally:
        config['DEFAULT']['last.update'] = ctime()
    return config


def ip_to_hash_filename(ip):
    """Encode a IPv4 and IPv6 to a filename
    for use with ip_info in /register.html
    """
    # Encode the IP address to bytes
    ip_bytes: bytes = ip.encode('utf-8')
    # Create a SHA-256 hash object
    hash_object: hashlib = hashlib.sha256(ip_bytes)
    # Get the hexadecimal representation of the hash
    hash_filename = hash_object.hexdigest()
    f_file: str = path.join(expanduser('~'),'www','app','ip_reg',hash_filename + '.ini')
    return f_file

def ip_reg_check(client_ip) -> ConfigParser:
    """Downloads IP information and checks for threat.
    Updates the data after 15 hours prior to a check.
    Saves the data in a IP hashlib ini filename
    located in ~/wwww/app/ip_reg/iphashes-filenames.ini
    and settings file such as API_KEY in ~/www/app/ipreg.ini
    """
    for letter in client_ip:
        if letter.isalnum() or letter == '-' or letter == '_' or letter == '.':
            pass
    else:
        return
    ip_info: ConfigParser = ConfigParser()
    ip_file: str = ip_to_hash_filename(client_ip)   # Hashes the IP for filename
    try:
        ip_info.read(ip_file)
        if 'DEFAULT' in ip_info.keys():
            if ip_info['DEFAULT'].has_section('last.update'):
                if ip_is_bad(ip_info):
                    raise IP_is_Bad
                if int(ctime()) - int(ip_info['DEFAULT']['last.update']) > 60 * 60 * 15:
                    if delete_file(ip_file) is False:
                        # There was an error deleting the file
                        # and it probably cannot be written to.
                        pass
                    else:
                        j_data: dict = get_ip_info(client_ip)
                        ip_info = dict_to_configparser(j_data)
        if ip_info:
            with open(ip_file,'w') as fp:
                ip_info.write(fp, space_around_delimiters = True)
            flash('It Worked!! Attacker is: '+ip_info['security']['is_attacker'])
        else:
            pass
    except IP_is_Bad:
        raise
    except Exception:
        pass
    return ip_info


def ip_is_bad(ip_info):
    if str(ip_info['security']['is_attacker']).lower() == 'true' \
    or str(ip_info['security']['is_abuser']).lower() == 'true' \
    or str(ip_info['security']['is_threat']).lower() == 'true' \
    or str(ip_info['security']['is_bogon']).lower() == 'true':
        raise IP_is_Bad

class IP_is_Bad(Exception):
    pass


def get_ip_checked(req):
    # Get IP from 'X-Forwarded-For' header
    client_ip = req.headers.get('X-Forwarded-For')
    if client_ip:
        # If there are multiple IPs, take the first one
        xsplit = client_ip.split(',')
        if len(xsplit) > 3:
            ip_reg_check(xsplit[0])
        else:
            for ip in xsplit:
                ip = ip.strip()
                ip_reg_check(ip)

    client_ip = req.headers.get('X-Real-IP')
    if client_ip:
        ip_reg_check(client_ip)

    client_ip = req.headers.get('Forwarded')
    if client_ip:
        ip_reg_check(client_ip)

    ip_reg_check(req.remote_addr)
    return client_ip

@auth.route('/register/index.html', methods=['GET', 'POST'])
@auth.route('/register/', methods=['GET', 'POST'])
@auth.route('/registry.html', methods=['GET', 'POST'])
@auth.route('/registry/register.html', methods=['GET', 'POST'])
@auth.route('/registry/index.html', methods=['GET', 'POST'])
@auth.route('/register.html', methods=['GET', 'POST'])
@limiter.limit("16 per minute")
def register():
    gk.report()
    xsearch=xSearchForm()
#    try:
#        client_ip = get_ip_checked(request)
#    except IP_is_Bad:
#        flash('You are not allowed to login nor register')
#        return redirect('/index.html', code=307)
#    except Exception:
#        pass
    if request.method == 'POST':
        session['logged_in'] = False
        email: [bool, str] = request.form.get('email')
        username: [bool, str] = request.form.get('username').strip(' \n\x0c\t\f')
        passwd: [bool, str] = request.form.get('password').strip(' \n\x0c\t\f')
        q1_q: [bool, str] = request.form.get('q1_q')
        q1_a: [bool, str] = request.form.get('q1_a')
        q2_q: [bool, str] = request.form.get('q2_q')
        q2_a: [bool, str] = request.form.get('q2_a')
        user_pass = username + ':' + passwd
        username_check = validate_email_or_login(user_pass, email = False)
        email_check = validate_email_or_login(email, email = True)
        if not email_check:
            flash("You must enter your real email address; to verify it.")
            return render_template("register.html", xsearch=xsearch)
        elif not username_check:
            flash('Minimum <b>EiGhT</b> <u>alphanumeric</u> characters; no <u>banned</u> words/ones or zeros.', category='error')
            return render_template("register.html", xsearch=xsearch)
        else:
            del user_pass
            del username_check
            del email_check
            # put xsearch below: done
            # return Response('These are the items username='+username+' passwd='+passwd+' q1_q='+q1_q+' q1_a='+q1_a+' q2_q='+q2_q+' q2_a='+q2_a, status=200, mimetype='text/plain')
            return register_user_post(username, passwd, email, q1_q, q1_a, q2_q, q2_a, power='normal')
    return render_template("register.html", xsearch=xsearch)


@auth.route('/quest.html', methods=['GET', 'POST'])
@auth.route('/question.html', methods=['GET', 'POST'])
@auth.route('/questions.html', methods=['GET', 'POST'])
def question_form():
    """
        This page will show the security questions associated with the accounts
        username or email address that is provided.
        The page renders the the e-mail, usernames, and the security questions,
        or reedirects back to forogt.html with a flash of the reason it failed
        to render questions.html. Questions.html is where the questions get
        answered, however they are processed with 'def answer_form()'
        via 'answered.html'
    """
    gk.report()
    xsearch=xSearchForm()
    if request.method == 'POST':
        session['logged_in'] = False
        user_email: str = request.form.get('user_email')
        username: str | bool = request.form.get('username')
        goodemail: bool | str = True
        goodemail = validate_email_or_login(user_email, email = True)
        gooduser: bool | str = validate_email_or_login(username, email = False)
        if not goodemail or not gooduser:
            flash('<a href="https://simple.wikipedia.org/wiki/Alphanumeric">Alphabetic</a> and <u>digit</u> characters only. Not <b>ones</b> nor <b>zeros</b>.', category='error')
            # render forgot.html
        else:
            found_user, found_email, found_q1, found_q2 = fetch_user_by_detail(detail = goodemail)
            if found_user is False:
                flash("No user accounts match your input")
                # render forgot.html
            else:
                return render_template("questions.html", user=found_user, email=found_email, q1_q=found_q1[0], q2_q=found_q2[0], xsearch=xsearch)
    return render_template("forgot.html", xsearch=xsearch)

