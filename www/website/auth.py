from flask import Blueprint, render_template, make_response

from flask import request, flash, redirect
#from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

from . import login_user_post, register_user_post, save_user, load_users_ini, strip_html, checkAlnum

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
            return render_template('proxies.html', bnc_list=proxy_list, passcode='password')
    return render_template('proxy-login.html')

passcodes = {}
@auth.route("/login/", methods=["POST", "GET"])
@auth.route("/login.html", methods=["POST", "GET"])
def login():
    if 'logged_in' in session.keys() and session['logged_in'] == 'True':
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
            flash('UserName or password fields are blank?', category='error')
            return make_response(render_template("login.html"), 401)
        elif username[1] or passw[1]:
            flash("UserName and Password fields must be alphanumeric only.", category='error')
            return make_response(render_template("login.html"), 401)
        else:
            return login_user_post(username[0], passw[0])
    return make_response(render_template("login.html"), 401)



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
        gooditem: bool = True
        gooditem = checkAlnum(username)
        if gooditem == True:
            gooditem = checkAlnum(pass1)
        if gooditem == True:
            gooditem = checkAlnum(pass2)
        if not gooditem:
            flash('You must use alphabetic and digit characters only.', category='error')
            return render_template("register.html")
        else:
            return register_user_post(username, pass1, pass2)
