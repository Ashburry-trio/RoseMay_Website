from flask import Blueprint, render_template, make_response

from flask import request, flash, redirect
#from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from os import path
navfix = Blueprint('navfix', __name__, template_folder='templates', static_folder='static')




