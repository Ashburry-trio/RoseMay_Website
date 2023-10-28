from flask import Blueprint, send_from_directory
from flask_app import gk
search_engines = Blueprint('search_engines', __name__, template_folder='templates', static_folder='static')

@search_engines.route('/site.webmanifest', methods=['GET'])
def web_manifest():
    gk.report()
    send_from_directory('static', 'site.webmanifest')

@search_engines.route('/favicon.ico', methods=['GET'])
def se_favicon():
    gk.report()
    send_from_directory('static', 'favicon.ico')

@search_engines.route('/mstile-144x144.ico', methods=['GET'])
def se_mstile():
    gk.report()
    send_from_directory('static', 'mstile-144x144.ico')

@search_engines.route('/apple-touch-icon.ico', methods=['GET'])
def se_appletouch():
    gk.report()
    send_from_directory('static', 'apple-touch-icon.ico')

@search_engines.route('/android-chrome-512x512.ico', methods=['GET'])
def se_achrome1():
    gk.report()
    send_from_directory('static', 'android-chrome-512x512.ico')

@search_engines.route('/android-chrome-192x192.ico', methods=['GET'])
def se_acrhome2():
    gk.report()
    send_from_directory('static', 'android-chrome-192x192.ico')
