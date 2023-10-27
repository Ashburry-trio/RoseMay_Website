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
from website import load_casino_user, save_casino_app, load_casino_app
from .date_func import update_today
from decimal import Decimal
casino = Blueprint('casino', __name__, template_folder='templates', static_folder='static')
from flask_app import gk

stash: list[str, str] = ['$0.00 CAD', '0.00']
stash_load: list[int] = [0]

def load_stash():
    casino_app = load_casino_app()
    stash[1] = str(casino_app['casino']['safe'])
    stash[0] = '$' + str(stash[1]) + ' CAD'

def save_stash():
 casino_app = load_casino_app()
 casino_app['casino']['safe'] = stash[1]
 save_casino_app()

def apply_stash(amount: str):
    stash_amount = Decimal(stash[1])
    apply_amount = Decimal(amount)
    stash[1] = str(stash_amount + apply_amount)
    stash[0] = '$' + str(stash[1]) + ' CAD'
    save_stash()


@casino.route('/casino/', methods=['GET', 'POST'])
@casino.route('/casino/index.html', methods=['GET', 'POST'])
@casino.route('/casino/casino.html', methods=['GET', 'POST'])
@casino.route('/casino/games.html', methods=['GET', 'POST'])
def casino_home():
    gk.report()
    update_today()
    load_stash()
    casino_user = load_casino_user()
    global stash
    if casino_user is False:
        cash = '<a href="/login.html" alt="click to sign-in to mSLscript.com account.">to Log-in</a>'
        prize_cash = 'unknown amount'
        remaining_pages = 9
    else:
        cash = '$' + str(casino_user['main']['cash_in']) + ' CAD'
        prize_cash = '$' + str(casino_user['main']['prize_cash']) + ' CAD'
        remaining_pages = int(casino_user['main']['remaining_pages'])
    return render_template('/casino/index.html', stash=stash[0], cash=cash, prize_cash=prize_cash,remaining_pages=remaining_pages)


@casino.route('/casino/prizes.html', methods=['GET'])
@casino.route('/casino/prizes/', methods=['GET'])
@casino.route('/casino/prizes/index.html', methods=['GET'])
def peak_prizes():
    gk.report()
    try:
        load_stash()
        update_today()
        casino_user = load_casino_user()
        global stash
        if casino_user is False:
            cash = '<a href="/login.html" alt="click to sign-in to mSLscript.com account.">to Log-in</a>'
            prize_cash = 'unknown money amount'
            remaining_pages = 9
            return render_template('/casino/prizes.html', stash=stash[0], cash=cash, prize_cash=prize_cash,remaining_pages=remaining_pages)
        else:
            cash = '$' + str(casino_user['main']['cash_in']) + ' CAD'
            prize_cash = '$' + str(casino_user['main']['prize_cash']) + ' CAD'
            remaining_pages = int(casino_user['main']['remaining_pages'])
            return render_template('/casino/prizes.html', stash=stash[0], cash=cash, prize_cash=prize_cash,remaining_pages=remaining_pages)
    except (KeyError, ValueError):
        cash = '<a href="/login.html" alt="click to sign-in to mSLscript.com account.">to Log-in</a>'
        prize_cash = 'unknown money amount'
        remaining_pages = 9
        return render_template('/casino/prizes.html', stash=stash[0], cash=cash, prize_cash=prize_cash,remaining_pages=remaining_pages)

@casino.route('/casino/locked/', methods=['GET'])
@casino.route('/casino/locked/games.html', methods=['GET'])
def lockedASAD_games():
    gk.report()
    load_stash()
    update_today()
    casino_user = load_casino_user(session['username'])
    if casino_user is False:
        flash('you must login to view the locked games.')
        return redirect("/register.html", code=307)
    elif 'username' in session.keys():
        cash = '$' + str(casino_user['main']['cash_in']) + ' CAD'
        prize_cash = '$' + str(casino_user['main']['prize_cash']) + ' CAD'
        remaining_pages = int(casino_user['main']['remaining_pages'])
        if remaining_pages >= 1:
            return render_template('/casino/locked.html', stash=stash[0], cash=cash, prize_cash=prize_cash,remaining_pages=remaining_pages)
        elif remaining_pages <= 0:
            return render_template('/casino/unlocked.html', stash=stash[0], cash=cash, prize_cash=prize_cash,remaining_pages=remaining_pages)
    else:
        cash = '<a href="/login.html" alt="click to sign-in to mSLscript.com account.">to Log-in</a>'
        prize_cash = 'unknown money amount'
        remaining_pages = 9
        return render_template('/casino/locked.html', stash=stash[0], cash=cash, prize_cash=prize_cash,remaining_pages=remaining_pages)

@casino.route('/casino/bank.html', methods=['GET'])
@casino.route('/casino/banker.html', methods=['GET'])
@casino.route('/casino/bank/', methods=['GET'])
@casino.route('/casino/banker/', methods=['GET'])
def casino_banker():
    gk.report()
    try:
        load_stash()
        update_today()
        if 'username' in session.keys():
            casino_user = load_casino_user()
            cash = '$' + str(casino_user['main']['cash_in']) + ' CAD'
            prize_cash = '$' + str(casino_user['main']['prize_cash']) + ' CAD'
            remaining_pages = int(casino_user['main']['remaining_pages'])
            return render_template('/casino/bank.html', stash=stash[0], cash=cash, prize_cash=prize_cash,remaining_pages=remaining_pages)
        else:
            raise KeyError
    except KeyError:
        cash = '<a href=\"/login.html\" alt=\"click to sign-in to mSLscript.com account.\">to Log-in</a>'
        prize_cash = 'unknown money amount'
        remaining_pages = 9
        return render_template("/casino/bank.html", stash=stash[0], cash=cash, prize_cash=prize_cash,remaining_pages=remaining_pages)

