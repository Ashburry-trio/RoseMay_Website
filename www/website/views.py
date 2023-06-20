from flask import (
    Blueprint, render_template, request, flash, make_response
    )
from flask import redirect, session

views = Blueprint('views', __name__, template_folder='templates', static_folder='static')

@views.route('/', methods=['GET', 'POST'])
@views.route('/index.html', methods=['GET', 'POST'])
def index_home():
    return render_template('index.html')


@views.route('/license/zero-bsd.html', methods=['GET'])
@views.route('/license/', methods=['GET'])
@views.route('/zero-bsd.html', methods=['GET'])
def zero_bsd():
    return render_template('zero-bsd.html')


@views.route('/coc/code_of_conduct.html', methods=['GET'])
@views.route('/code_of_conduct.html', methods=['GET'])
@views.route('/coc/', methods=['GET'])
@views.route('/coc.html', methods=['GET'])
def coc():
    return render_template('coc.html')


@views.route('/contrib.html', methods=['GET'])
@views.route('/contributing', methods=['GET'])
@views.route('/contrib/', methods=['GET'])
@views.route('/contributing.html', methods=['GET'])
def contrib():
    return render_template('contributing.html')


@views.route('/security.html', methods=['GET'])
@views.route('/security', methods=['GET'])
def security():
    return render_template('security.html')


@views.route('/download.html', methods=['GET'])
@views.route('/download/', methods=['GET'])
def download_msl():
    return render_template('download.html')
