#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import annotations

from flask import Blueprint, render_template, request, flash, make_response, url_for
from flask import redirect, session
from os import path
#from sys import path as syspath
from time import time as timesecs
_dir = path.dirname(path.abspath(__file__))
# if not _dir in syspath:
#     syspath.append(_dir)
from . import load_casino_user, save_casino_app, load_casino_app
from .date_func import update_today
from decimal import Decimal
casino = Blueprint('casino', __name__, template_folder='templates', static_folder='static')

stash: list[str, str] = ['$0.00 CAD', '0.00']
stash_load: list[int] = [0]

def load_stash():
    if int(timesecs()) - stash_load[0] < 1500:
        return
    casino_app = load_casino_app()
    stash[1] = str(casino_app['casino']['safe'])
    stash[0] = '$' + str(stash[1]) + ' CAD'
    stash_load[0] = int(timesecs())

def save_stash():
 casino_app = load_casino_app()
 casino_app['casino']['safe'] = stash[1]
 save_casino_app()

def apply_stash(amount: str):
    stash_amount = Decimal(stash[1])
    apply_amount = Decimal(amount)
    stash[1] = str(stash_amount + apply_amount)
    stash[0] = '$' + str(stash[1]) + ' CAD'

@casino.route('/casino/', methods=['GET', 'POST'])
@casino.route('/casino.html', methods=['GET', 'POST'])
@casino.route('/casino/index.html', methods=['GET', 'POST'])
@casino.route('/casino/casino.html', methods=['GET', 'POST'])
@casino.route('/casino/games.html', methods=['GET', 'POST'])
def casino_home():
    update_today()
    load_stash()
    casino_user = load_casino_user()
    if casino_user == False:
        cash = 'to Log-in'
    else:
        cash = '$' + str(casino_user['main']['cash-in']) + ' CAD'
    return render_template('/casino/index.html', stash=stash[1], cash=cash)

@casino.route('/casino/prizes.html', methods=['GET'])
@casino.route('/casino/prizes/', methods=['GET'])
@casino.route('/casino/prizes/index.html', methods=['GET'])
def peak_prizes():
    try:
        load_stash()
        update_today()
        return render_template('/casino/prizes.html', stash=stash[1])
    except BaseException:
        return

@casino.route('/casino/locked/index.html', methods=['GET'])
@casino.route('/casino/locked/', methods=['GET'])
@casino.route('/casino/locked/games.html', methods=['GET'])
def locked_games():
    try:
        load_stash()
        update_today()
        if 'username' in session.keys():
            casino_user = load_casino_user()
            pages = 9 - int(casino_user['main']['pages-visted'])
            if casino_user['main']['visited-9-pages'] != 'yes':
                return render_template('/casino/locked.html', stash=stash[1], pages_count=pages)
            else:
                return render_template('/casino/unlocked.html', stash=stash[1])
        flash('you must login to view the locked games')
        return redirect('/login.html')
    except KeyError:
        return render_template('/casino/locked.html')

class Table():
    users = []
    def __init__(self):
        self.owner = session['username']
        all_tables.append(self)


@casino.route('/casino/blackjack/new_table.html', methods=['GET', 'POST'])
def new_table():
    nt = Table()
    all_tables.append(nt)
    return render_template('index.html', all_tables = all_tables,this_table = nt)


class InvalidPlayers(Exception):
    pass