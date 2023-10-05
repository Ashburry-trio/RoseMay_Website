from flask import Blueprint, render_template, make_response

from flask import request, flash, redirect
#from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from os import path
navfix = Blueprint('navfix', __name__, template_folder='templates/sticky-footer-navbar', static_folder='static/assets')


@navfix.route('//', methods = ['GET'])
@navfix.route('/index.html', methods = ['GET'])
@navfix.route('/', methods = ['GET'])
def index_home_page():
    return render_template('index.html')


@navfix.route('/assets/<path:filename>')
def assetsCSS_JS(filename):
    return send_from_directory(navfix.static_folder, filename)


@navfix.route('sticky-navbar-footer.css', methods=['GET'])
def navfixcss():
    return render_template('sticky-navbar-footer.css')


@navfix.route('/testy')
def sometestyfx():
    return render_template('sticky-footer-navbar/index.html')