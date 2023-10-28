from flask import (
    Blueprint, render_template, make_response, Response, jsonify
    )
from werkzeug.exceptions import TooManyRequests
from flask_app import gk, app
views = Blueprint('views', __name__, template_folder='templates', static_folder='static')

@app.errorhandler(TooManyRequests)
def handle_rate_limit_exceeded(e):
    return jsonify({'error': 'Rate limit exceeded'}), 429

@views.route('/casino.html', methods=['GET', 'POST'])
@gk.specific(rate_limit_rules=[{"count":1,"window":1,"duration":240}])
def skinners_version_ignore():
    gk.report()
    response = Response('You have been banned for visiting this page. You probably found this page in someones "/ctcp bauderr_ version" reply. This is a danger person who you should ignore.', status=429, mimetype='text/plain')
    return response

@views.route('/.well-known/', methods=['GET', 'POST'])
@views.route('//wp-includes/wlwmanifest.xml', methods=['GET', 'POST'])
@views.route('//xmlrpc.php', methods=['GET', 'POST'])
@views.route('//blog/wp-includes/wlwmanifest.xml', methods=['GET', 'POST'])
@views.route('//web/wp-includes/wlwmanifest.xml', methods=['GET', 'POST'])
@views.route('//wordpress/wp-includes/wlwmanifest.xml', methods=['GET', 'POST'])
@views.route('//website/wp-includes/wlwmanifest.xml', methods=['GET', 'POST'])
@views.route('//wp/wp-includes/wlwmanifest.xml', methods=['GET', 'POST'])
@views.route('//news/wp-includes/wlwmanifest.xml', methods=['GET', 'POST'])
@views.route('//2018/wp-includes/wlwmanifest.xml', methods=['GET', 'POST'])
@views.route('//2019/wp-includes/wlwmanifest.xml', methods=['GET', 'POST'])
@views.route('//shop/wp-includes/wlwmanifest.xml', methods=['GET', 'POST'])
@views.route('//wp1/wp-includes/wlwmanifest.xml', methods=['GET', 'POST'])
@views.route('//test/wp-includes/wlwmanifest.xml', methods=['GET', 'POST'])
@views.route('//media/wp-includes/wlwmanifest.xml', methods=['GET', 'POST'])
@views.route('//wp2/wp-includes/wlwmanifest.xml', methods=['GET', 'POST'])
@views.route('//site/wp-includes/wlwmanifest.xml', methods=['GET', 'POST'])
@views.route('//cms/wp-includes/wlwmanifest.xml', methods=['GET', 'POST'])
@views.route('//sito/wp-includes/wlwmanifest.xml', methods=['GET', 'POST'])
@views.route('/administrator/index.php', methods=['GET', 'POST'])
@views.route('/view-source:', methods=['GET', 'POST'])
@views.route('/misc/ajax.js', methods=['GET', 'POST'])
@views.route('/wp-login.php', methods=['GET', 'POST'])
@gk.specific(rate_limit_rules=[{'count': 1, 'window': 60,"duration":240}])
def well_known_trap():
    gk.report()
    return make_response(render_template('banned.txt'), 429)

@views.route('/', methods=['GET'])
@views.route('/index.html', methods=['GET'])
def index_home():
    gk.report()
    return render_template('index.html')


@views.route('/hosted.html', methods=['GET'])
@views.route('/hosted/', methods=['GET'])
def hosted_info():
    gk.report()
    return render_template('hosted.html')


@views.route('/license/zero-bsd.html', methods=['GET'])
@views.route('/license/', methods=['GET'])
@views.route('/zero-bsd.html', methods=['GET'])
def zero_bsd():
    gk.report()
    return render_template('zero-bsd.html')


@views.route('/coc/code_of_conduct.html', methods=['GET'])
@views.route('/code_of_conduct.html', methods=['GET'])
@views.route('/coc/', methods=['GET'])
@views.route('/coc.html', methods=['GET'])
def coc():
    gk.report()
    return render_template('coc.html')


@views.route('/contributing/', methods=['GET'])
@views.route('/contrib/', methods=['GET'])
@views.route('/contributing.html', methods=['GET'])
@views.route('/contrib.html', methods=['GET'])
def contrib():
    gk.report()
    return render_template('contributing.html')


@views.route('/security.html', methods=['GET'])
@views.route('/security/', methods=['GET'])
def security():
    gk.report()
    return render_template('security.html')


@views.route('/download.html', methods=['GET'])
@views.route('/download/', methods=['GET'])
def download_msl():
    gk.report()
    return render_template('download.html')



