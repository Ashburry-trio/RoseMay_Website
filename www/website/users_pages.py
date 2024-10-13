from flask import (
    Blueprint, render_template, flash
    )
from flask import redirect, session
from website import user_page_exists, get_user_pages
from flask_app import gk
from os import mkdir
#from .reload import *
from website import load_users_ini, users
users_pages = Blueprint('users_pages', __name__, template_folder='templates', static_folder='static')

@users_pages.route('/user/<user>/admin.html', methods=['GET'])
@users_pages.route('/user/<user>/admin/', methods=['GET'])
def user_admin_page(user):
    gk.report()
    users = load_users_ini()
    user = users['username'].lower()
    while '.' in user:
        user = user.replace('.','')
    while '\\' in user:
        user = user.replace('\\','')
    if 'username' not in users.keys():
        flash("You must be signed-in to use this service.")
        return redirect("/register.html")
    user_up: str = users['username']
    if user_page_exists(user):
        return render_template('/users/'+ user + '/admin.html', user_up=user_up)


@users_pages.route('/user/<user>/', methods=['GET'])
@users_pages.route('/user/<user>/index.html', methods=['GET'])
def user_index_pages(user):
    gk.report()
    while '.' in user:
        user = user.replace('.','')
    while '\\' in user:
        user = user.replace('\\','')
    user_low = user.lower()
    del user
    has_page: bool = user_page_exists(user_low)
    if has_page:
        load_users_ini()
        user_up = users['main']['username']

        return render_template('/users/'+user_low + '/index.html',user_up=user_up)
    else:
        return redirect('/user/nobody.html')


@users_pages.route('/nobody/', methods=['GET'])
@users_pages.route('/nobody.html', methods=['GET'])
@users_pages.route('/user/nobody.html', methods=['GET'])
@users_pages.route('/user/', methods=['GET'])
def no_user_page():
    gk.report()
    has_page: bool = None
    user_up: str = None
    if 'username' in session.keys():
        user_up = session['username']
    asset_list: tuple[tuple[str, str, tuple[str]], tuple[str, str, tuple[str]]] = get_user_pages()
    return render_template('users/nobody.html', user_up=user_up, has_page=has_page, assets=asset_list)


@users_pages.route('/user/', methods=['GET'])
@users_pages.route('/user/create.html', methods=['GET'])
@users_pages.route('/create.html', methods=['GET'])
@users_pages.route('/create/', methods=['GET'])
def user_create_page():
    gk.report()
    has_page: bool
    # return Response("This page has not been created, yet; much like all of this site. But eventually it will be finished and it will be large")