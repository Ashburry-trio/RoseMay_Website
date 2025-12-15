from cryptography.fernet import Fernet
from flask import (
    Blueprint, render_template, make_response, Response, jsonify, redirect,
    send_file, url_for, session, request
    )
from flask_wtf.csrf import CSRFError
from werkzeug.exceptions import TooManyRequests
from os.path import expanduser
from markupsafe import escape
from flask_app import app
from website import xSearchForm
views = Blueprint('views', __name__, template_folder='templates', static_folder='static')

@app.route("/test1")
def login():
    return render_template("test.html")

@app.route('/site.webmanifest')
def manifest():
    return jsonify({
        "name": "PyNet Converge script named Bauderr",
        "short_name": "Pync",
        "start_url": url_for('views.index_home', _external=True),  # dynamically set start_url
        "display": "browser",
        "background_color": "#DAA520",
        "theme_color": "#DAA520",
        "description": "An mSL script for mIRC ($20) and Adiirc (FREE) chat clients which will connect to a http/1.0 CONNECT proxy-server (hosted by me) for awesome and fast functionality.",
        "icons": [
            {
            "src": "/static/custom/brand/android-chrome-192x192.png",
            "sizes": "192x192",
            "type": "image/png"
            },
            {
            "src": "/static/custom/brand/android-chrome-512x512.png",
            "sizes": "512x512",
            "type": "image/png"
            },
            {
            "src": "/static/custom/brand/apple-touch-icon.png",
            "sizes": "180x180",
            "type": "image/png"
            },
            {
            "src": "/static/custom/brand/mstile-144x144.png",
            "sizes": "144x144",
            "type": "image/png"
            },
            {
            "src": "/static/custom/brand/favicon.png",
            "sizes": "16x16",
            "type": "image/png"
            },
            {
            "src": "/static/custom/brand/repository-open-graph-template.png",
            "sizes": "16x16",
            "type": "image/png"
            },
            {
            "src": "/static/custom/brand/safari-pinned-tab.png",
            "sizes": "16x16",
            "type": "image/png"
            }
        ]
    }
)
@views.route('/stocks.py', methods=['GET'])
def stocks():
    return send_file(expanduser('~/www/stocks.py'), as_attachment=True, download_name='stocks.py'), 200

@views.route('/parse_stocks.py', methods=['GET'])
def parse_stocks():
    return send_file(expanduser('~/www/parse_stocks.py'), as_attachment=True, download_name='parse_stocks.py'), 200

@views.route('/mywotdddf72ca09e4c80ba89a.html', methods=['GET'])
def mywotddd():
    # Change this to your own Web of Trust file
    return send_file(expanduser('~/www/website/static/custom/mywotdddf72ca09e4c80ba89a.html')), 200

@views.route('/fo-verify.html', methods=['GET'])
def flexoffers():
    # This is to verify flexoffers.com account
    return send_file(expanduser('~/www/website/static/custom/fo-verify.html')), 200

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
#    gk.report()
    xsearch = xSearchForm()
    return render_template('csrf_error.html', xsearch=xsearch), 400

@app.errorhandler(TooManyRequests)
def handle_rate_limit_exceeded(e):
    return jsonify({'tooManyRequests': 'the webserver is flooded with traffic. Try again, whenever you are ready...' }), 429

@app.errorhandler(404)
def no_found(e):
#    gk.report()
    xsearch = xSearchForm()
    return render_template('404.html', xsearch=xsearch), 404

@views.route('/.well-known/apple-developer-merchantid-domain-association', methods=['GET'])
def apple_deveoper_merch():
    return send_file(expanduser('~/www/website/static/custom/apple-developer-merchantid-domain-association')), 200

@views.route('/_asterisk/', methods=['GET', 'POST'])
@views.route('/admin/assets/js/views/login.js', methods=['GET', 'POST'])
@views.route('/admin/images/cal_date_over.gif', methods=['GET', 'POST'])
@views.route('/ajax/', methods=['GET', 'POST'])
@views.route('/api/v1/pods/', methods=['GET', 'POST'])
@views.route('/bea_wls_deployment_internal/', methods=['GET', 'POST'])
@views.route('/HNAP1//', methods=['GET', 'POST'])
@views.route('/index.php/admin/', methods=['GET', 'POST'])
@views.route('/jenkins/login/', methods=['GET', 'POST'])
@views.route('/joomla/', methods=['GET', 'POST'])
@views.route('/libs/js/iframe.js', methods=['GET', 'POST'])
@views.route('/manager/html/', methods=['GET', 'POST'])
@views.route('/muieblackcat/', methods=['GET', 'POST'])
@views.route('/myadmin/', methods=['GET', 'POST'])
@views.route('/mysqladmin/', methods=['GET', 'POST'])
@views.route('/phpmyadmin/', methods=['GET', 'POST'])
@views.route('/phpmyadmin1/', methods=['GET', 'POST'])
@views.route('/phpmyadmin0/', methods=['GET', 'POST'])
@views.route('/pma/', methods=['GET', 'POST'])
@views.route('/remote/login/', methods=['GET', 'POST'])
@views.route('/sftp-config.json', methods=['GET', 'POST'])
@views.route('/solr/', methods=['GET', 'POST'])
@views.route('/TP/public/index.php', methods=['GET', 'POST'])
@views.route('/sql/', methods=['GET', 'POST'])
@views.route('/temp/wp-admin/', methods=['GET', 'POST'])
@views.route('/templates/system/css/system.css', methods=['GET', 'POST'])
@views.route('/wp-content/plugins/image-clipboard/readme.txt', methods=['GET', 'POST'])
@views.route('/api/jsonws/invoke/', methods=['GET', 'POST'])
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
@views.route('/wizard/', methods=['GET', 'POST'])
@views.route('/WebInterface/function/', methods=['GET', 'POST'])
@views.route('/WebInterface/', methods=['GET', 'POST'])
@views.route('/sabnzbd/', methods=['GET', 'POST'])
@views.route('/sabnzbd/wizard/', methods=['GET', 'POST'])
# @gk.specific(rate_limit_rules=[{'count': 1, 'window': 60,"duration":2400}])
def well_known_trap():
#    gk.report()
    return make_response(app.send_static_file('banned.txt'), 403)


@views.route('/leakygut.html')
def fixbiome():
    return redirect('https://shop.fixbiome.com/ref/31/', code=302)

@views.route('/home.html', methods=['GET', "POST"])
@views.route('/index/', methods=['GET', "POST"])
@views.route('/index.htm', methods=['GET', "POST"])
@views.route('/', methods=['GET', "POST"])
@views.route('/index.html', methods=['GET', "POST"])
def index_home():
#    gk.report()
    xsearch = xSearchForm()
    return render_template('index.html', xsearch=xsearch, content_page_name='home')

@views.route('/pinterest-cd548.html', methods=['GET'])
def pinterest():
    return app.send_static_file('pinterest-cd548.html')



@views.route('/index2.html', methods=["GET", "POST"])
def index2_home():
#    gk.report()
    xsearch = xSearchForm()
    return render_template('index2.html', xsearch=xsearch, content_page_name='home')

@views.route('/index3.html', methods=['GET', "POST"])
def index3_home():
#    gk.report()
    xsearch = xSearchForm()
    return render_template('index3.html', xsearch=xsearch, content_page_name='home')


@views.route('/test.html', methods=['GET', "POST"])
def index_test():
#    gk.report()
    xsearch = xSearchForm()
    return render_template('test.html', xsearch=xsearch)



@views.route('/search.htm', methods=['GET', 'POST'])
@views.route('/xdcc/search.htm', methods=['GET', 'POST'])
@views.route('/search.html', methods=['GET', 'POST'])
@views.route('/xdcc/search.html', methods=['GET', 'POST'])
def xsearch_page():
    xsearch = xSearchForm()
    search_results = {}
    if xsearch.validate_on_submit():
        filesearch = escape(xsearch.search.data)
        filesearch = parse_xsearch_filename(filesearch)
        if len(filesearch) < 3 or len(filesearch) > 75:
            flash("Search term must be at least 3 characters and a max of 75 characters: " + str(len(filesearch)) + ' chars')
            return render_template("/search/search.html", content_page_name='xsearch', locations={}, xsearch=xsearch, search_results={}, found=False, error=True, error_type='length')
        else:
            pass
    return render_template("/search/search.html", content_page_name='xsearch', xsearch=xsearch, active_locations={}, search_all_locations=True, search_results=search_results, found=True, error=False, error_type='')


def parse_xsearch_filename(filesearch_no_space: str):
    filesearch_no_space = escape(filesearch_no_space)
    filesearch_no_space = filesearch_no_space.strip()
    filesearch_no_space = '*' + filesearch_no_space
    filesearch_no_space = filesearch_no_space.replace('  ', ' ')
    filesearch_no_space = filesearch_no_space.replace(' - ',' -')

    excluded_terms = filesearch_no_space[filesearch_no_space.find(' -',3):len(filesearch_no_space)].split('-')
    excluded_finished = []
    for fn in excluded_terms:
        excluded_finished.append(fn.strip())
    del fn
    filesearch_no_space = filesearch_no_space[0:filesearch_no_space.find(' -',3)]
    filesearch_no_space = filesearch_no_space.replace('~','')
    filesearch_no_space = filesearch_no_space.replace('-','.')
    filesearch_no_space = filesearch_no_space.replace(' ','.')
    filesearch_no_space = filesearch_no_space.replace('_','.')
    filesearch_no_space = filesearch_no_space.replace('\\','.')
    filesearch_no_space = filesearch_no_space.replace('/','.')
    filesearch_no_space = filesearch_no_space.replace(',','.')
    filesearch_no_space = filesearch_no_space.replace(';','.')
    filesearch_no_space = filesearch_no_space.replace('?','.')
    filesearch_no_space = filesearch_no_space.replace(':','.')
    filesearch_no_space = filesearch_no_space.replace('"','')
    filesearch_no_space = filesearch_no_space.replace('\'','')
    filesearch_no_space = filesearch_no_space.replace('[','.')
    filesearch_no_space = filesearch_no_space.replace(']','.')
    filesearch_no_space = filesearch_no_space.replace('{','.')
    filesearch_no_space = filesearch_no_space.replace('}','.')
    filesearch_no_space = filesearch_no_space.replace('(','.')
    filesearch_no_space = filesearch_no_space.replace(')','.')
    filesearch_no_space = filesearch_no_space.replace('+','.')
    filesearch_no_space = filesearch_no_space.replace('=','.')
    filesearch_no_space = filesearch_no_space.replace('!','.')
    filesearch_no_space = filesearch_no_space.replace('&','*and*')
    filesearch_no_space = filesearch_no_space.replace('^','.')
    filesearch_no_space = filesearch_no_space.replace('\`','')
    filesearch_no_space = filesearch_no_space.replace('..',' ')
    filesearch_no_space = filesearch_no_space.replace('..',' ')
    filesearch_no_space = filesearch_no_space.replace('..',' ')
    filesearch_no_space = filesearch_no_space.replace('.',' ')
    filesearch_no_space = filesearch_no_space.replace('   ',' ')
    filesearch_no_space = filesearch_no_space.replace('  ',' ')
    filesearch_no_space = filesearch_no_space.replace('  ',' ')
    filesearch_no_space = filesearch_no_space.replace('\t',' ')
    filesearch_no_space = filesearch_no_space.replace('*','')
    filesearch_no_space = filesearch_no_space.replace('*','')
    filesearch_no_space = filesearch_no_space.replace('*','')
    filesearch_no_space = filesearch_no_space.replace('?','')
    filesearch_no_space = filesearch_no_space.replace('?','')
    if not filesearch_no_space:
        return None
    return filesearch_no_space

#filesearch_no_space = filesearch_no_space.replace('~',' -')
#   return filesearch_no_space

@views.route('/hosted.html', methods=['GET', 'POST'])
@views.route('/hosted/', methods=['GET', 'POST'])
def hosted_info():
#    gk.report()
    xsearch = xSearchForm()
    return render_template('hosted.html', xsearch=xsearch)


@views.route('/license/zero-bsd.html', methods=['GET', 'POST'])
@views.route('/license/', methods=['GET', 'POST'])
@views.route('/zero-bsd.html', methods=['GET', 'POST'])
def zero_bsd():
#    gk.report()
    xsearch = xSearchForm()
    return render_template('zero-bsd.html', xsearch=xsearch)


@views.route('/coc/code_of_conduct.html', methods=['GET', 'POST'])
@views.route('/code_of_conduct.html', methods=['GET', 'POST'])
@views.route('/coc/', methods=['GET', 'POST'])
@views.route('/coc.html', methods=['GET', 'POST'])
def coc():
#    gk.report()
    xsearch = xSearchForm()
    return render_template('coc.html', xsearch=xsearch)


@views.route('/contributing/', methods=['GET', 'POST'])
@views.route('/contrib/', methods=['GET', 'POST'])
@views.route('/contributing.html', methods=['GET', 'POST'])
@views.route('/contrib.html', methods=['GET', 'POST'])
def contrib():
#    gk.report()
    xsearch = xSearchForm()
    return render_template('contributing.html', xsearch=xsearch)

@views.route('/privacypolicy/', methods=['GET', 'POST'])
@views.route('/privacy-policy/', methods=['GET', 'POST'])
@views.route('/policy/', methods=['GET', 'POST'])
@views.route('/privacypolicy.html', methods=['GET', 'POST'])
@views.route('/privacy-policy.html', methods=['GET', 'POST'])
@views.route('/policy.html', methods=['GET', 'POST'])
def policy():
#    gk.report()
    xsearch = xSearchForm()
    return render_template('policy.html', xsearch=xsearch)

@views.route('/security.html', methods=['GET', 'POST'])
@views.route('/security/', methods=['GET', 'POST'])
def security():
#    gk.report()
    xsearch = xSearchForm()
    return render_template('security.html', xsearch=xsearch)


@views.route('/download.html', methods=['GET', 'POST'])
@views.route('/download/', methods=['GET', 'POST'])
def download_msl():
#    gk.report()
    xsearch = xSearchForm()
    return render_template('download.html', content_page_name='download', xsearch=xsearch)

