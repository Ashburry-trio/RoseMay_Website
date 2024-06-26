from flask import Blueprint, render_template, make_response

from flask import request, flash, redirect
#from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from os import path
auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')
from flask_app import gk
from website import login_user_post, register_user_post, save_user, load_users_ini, strip_html, checkAlnum, users

@auth.route("/irc/script.html", methods=["POST", "GET"])
@auth.route("/irc/scripts.html", methods=["POST", "GET"])
@auth.route("/script/", methods=["POST", "GET"])
@auth.route("/scripts/", methods=["POST", "GET"])
@auth.route("/script.html", methods=["POST", "GET"])
@auth.route("/scripts.html", methods=["POST", "GET"])
def proxy_scripts():
    gk.report()
    if 'logged_in' in session.keys() and session['logged_in'] is True:
            return render_template(path.join('scripts', 'scripts.html'))
    else:
        return make_response(render_template(path.join('scripts', 'no-scripts.html')), 401)


@auth.route("/proxies/", methods=["POST", "GET"])
@auth.route("/proxy/", methods=["POST", "GET"])
@auth.route("/irc/proxy.html", methods=["POST", "GET"])
@auth.route("/irc/proxies.html", methods=["POST", "GET"])
@auth.route("/proxy.html", methods=["POST", "GET"])
@auth.route("/proxies.html", methods=["POST", "GET"])
def irc_proxies():
    gk.report()
    global users
    if 'logged_in' in session.keys() and session['logged_in'] is True:
        proxy_list: dict[str, str]
        users = load_users_ini(session['username'])
        proxy_list = users['proxy']
        return render_template('proxies.html', bnc_list=proxy_list, passcode=users['passcode']['secret'])
    else:
        return render_template('proxy-login.html')

@auth.route("/login/", methods=["POST", "GET"])
@auth.route("/login.html", methods=["POST", "GET"])
def login():
    gk.report()
    if 'logged_in' in session.keys() and session['logged_in'] is True:
        session['logged_in'] = False
        session['username'] = None
    if request.method == "POST":
        # record the user name
        username = request.form.get("username")
        passw = request.form.get("password")
        if not passw: passw = ''
        if not username: username = ''
        username = strip_html(username)
        passw = strip_html(passw)
        if not passw[0] or not username[0]:
            flash('UserName or Password fields are blank?', category='error')
        elif username[1] or passw[1]:
            flash("UserName and Password fields must be alphanumeric only.", category='error')
        else:
            load_users_ini(username[0].lower())
            return login_user_post(username[0], passw[0])
    return make_response(render_template("login.html"), 401)



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

@auth.route('/register/index.html', methods=['GET', 'POST'])
@auth.route('/register/', methods=['GET', 'POST'])
@auth.route('/register.html', methods=['GET', 'POST'])
def register():
    gk.report()
    if request.method == 'POST':
        session['logged_in'] = False
        username: str = request.form.get('username')
        passwd: str = request.form.get('password')
        gooditem: bool = True
        gooditem = checkAlnum(username)
        if gooditem is True:
            gooditem = checkAlnum(passwd)
        if not gooditem:
            flash('you must use alphabetic and digit characters only.', category='error')
            return render_template("register.html")
        else:
            return register_user_post(username, passwd)
    return render_template("register.html")

