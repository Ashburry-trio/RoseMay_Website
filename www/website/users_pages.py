from flask import (
    Blueprint, render_template, request, flash, make_response
    )
from flask import redirect, session, url_for
from os.path import isdir
from website import user_page_exists

users_pages = Blueprint('users_pages', __name__, template_folder='templates', static_folder='static')


@users_pages.route('/user/<user>/', methods=['GET'])
@users_pages.route('/user/<user>/index.html', methods=['GET'])
def user_home_pages(user):
    while '..' in user:
        user = user.replace('..','')
    while '\\' in user:
        user = user.replace('\\','')
    user_low = user.lower()
    del user
    has_page: bool = user_page_exists(user_low)
    if has_page:
        return render_template('users/'+user_low + '/index.html')
    else:
        return redirect('/user/nobody.html')

@users_pages.route('/user/nobody.html', methods=['GET'])
def no_user_page():
    has_page: bool
    if 'username' in session.keys():
        user_low: str = session['username'].lower()
        has_page = user_page_exists(user_low)
    else:
        has_page = False
    return render_template('users/nobody.html', has_page=has_page)

