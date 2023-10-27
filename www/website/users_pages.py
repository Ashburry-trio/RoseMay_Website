from flask import (
    Blueprint, render_template, flash
    )
from flask import redirect, session
from website import user_page_exists
from flask_app import gk
from .reload import reload
from website import load_users_ini, users
users_pages = Blueprint('users_pages', __name__, template_folder='templates', static_folder='static')


@users_pages.route('/user/<user>/admin.html', methods=['GET'])
@users_pages.route('/user/<user>/admin/', methods=['GET'])
def user_admin_page():
    gk.report()
    load_users_ini()
    while '.' in user:
        user = user.replace('.','')
    while '\\' in user:
        user = user.replace('\\','')
    if 'username' not in users.keys():
        flash("You must be signed-in to use this service.")
        redirect("/register.html")
    if users['username'] != user:
        flash("You can only admin your own user-page at /user/"+users['username']+"/admin.html")
        redirect("/user/"+user+"/admin.html")
    if user_page_exists(users['username']):
        return render_template('/users/'+users['username'] + '/admin.html')


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
        return render_template('/users/'+user_low + '/index.html')
    else:
        return redirect('/user/nobody.html')

@users_pages.route('/user/nobody.html', methods=['GET'])
@users_pages.route('/user/', methods=['GET'])
def no_user_pageasdf():
    gk.report()
    has_page: bool
    if 'username' in session.keys():
        user_low: str = session['username'].lower()
        has_page = user_page_exists(user_low)
    else:
        has_page = False
    return render_template('users/nobody.html', has_page=has_page)


@users_pages.route('/user/', methods=['GET'])
@users_pages.route('/user/create.html', methods=['GET'])
@users_pages.route('/create.html', methods=['GET'])
@users_pages.route('/create/', methods=['GET'])
def user_craete_page():
    gk.report()
    has_page: bool
    if 'username' in session.keys():
        user_low: str = session['username'].lower()
        has_page = user_page_exists(user_low)
    else:
        has_page = None
    if has_page == False:
        copytree('/home/Ashburry/www/website/templates/default_user','/home/Ashburry/www/website/templates/users/' + session['username'] +'/')
        has_page = True
        reload()
    return render_template('/create.html', has_page=has_page)
