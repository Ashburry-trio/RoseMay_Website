#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import annotations

from flask import session
#from dateutil.parser import parse
from datetime import datetime
from dateutil import tz
#from dateutil.relativedelta import relativedelta
from time import time as timesecs
#from os import path
from . import load_casino_user, save_casino_user


def update_today():
    this_year = datetime.now(tz.UTC).year
    if not '_casino-update' in session.keys() or this_year - session['_casino-update'] == 0:
        return
    session['_casino-update'] = this_year
    casino_user = load_casino_user()
    if not casino_user:
        return
    str_year = casino_user['main']['this_year']
    if this_year - str_year > 0:
        casino_user['main']['remaining_pages'] = '9'
        casino_user['main']['this_year'] = this_year
        save_casino_user()
