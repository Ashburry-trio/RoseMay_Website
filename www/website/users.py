from flask import (
    Blueprint, render_template, request, flash, make_response
    )
from flask import redirect, session
from os.path import isdir
from website import user_exists

users = Blueprint('users', __name__, template_folder='templates/users', static_folder='static')


@users.route('/users/<user>/', methods=['GET])
def user_home_pages(user):
    while '..' in user:
        user = user.replace('..','')
    while '/' in user:
        user = user.replace('/','')
    while '\' in user:
        user = user.replace('\','')
    user_low = user.lower()
    if user_exists(user_low|e):
        return render_template(user|e + '/index.html')
    else:
        return redirect('/nobody.html')

@users.route('/nobody.html', methods=['GET])
def no_user_page():
    return render_template('/users/nobody.html')

