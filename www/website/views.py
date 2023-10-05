from flask import (
    Blueprint, render_template, request, flash, make_response
    )
from flask import redirect, session
from time import time as secstime
views = Blueprint('views', __name__, template_folder='templates', static_folder='static')
banned = {}
@views.route('/.well-known/', methods=['GET'])
def well_known_trap():
    # 429 = too many requests
    banned[request.environ['REMOTE_ADDR']] = secstime()
    return make_response(render_template('banned.html'), 429)

def check_banned():
    baned_for: float
    banned[request.environ['REMOTE_ADDR']] = 3000
    if request.environ['REMOTE_ADDR'] in banned.keys():
        banned_for = secstime() - banned[request.environ['REMOTE_ADDR']]
        if banned_for > 5000:
            del banned[request.environ['REMOTE_ADDR']]
            return False
        else:
            return(False)
    else:
        return False

@views.route('/test2.html', methods=['GET'])
def test2():
    return render_template('test2.html')





@views.route('/hosted.html', methods=['GET'])
@views.route('/hosted/', methods=['GET'])
def hosted_info():
    if (check_banned()):
        return render_template('banned.txt')
    else:
        return render_template('hosted.html')



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

