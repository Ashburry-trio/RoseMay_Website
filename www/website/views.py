from flask import (
    Blueprint, render_template, make_response, Response, jsonify, redirect, send_file, url_for
    )
from werkzeug.exceptions import TooManyRequests
from os.path import expanduser
from markupsafe import escape
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length, DataRequired
from flask_app import gk, app

views = Blueprint('views', __name__, template_folder='templates', static_folder='static')


class xSearchForm(FlaskForm):
    search = StringField('XDCC Search',
                         render_kw={"class": "form-control me-2", "placeholder": "XDCC Search", "aria-label": "Search"},
                         validators=[DataRequired()])
    search_button = SubmitField('Search', render_kw={"class": "btn btn-outline-success", "type": "submit"})

@views.route('/mywotdddf72ca09e4c80ba89a.html', methods=['GET','POST'])
def mywotddd():
    # Change this to your own Web of Trust file
    return send_file(expanduser('~/www/website/static/mywotdddf72ca09e4c80ba89a.html')), 200

@views.route('/fo-verify.html', methods=['GET','POST'])
def flexoffers():
    # This is to verify flexoffers.com account
    return send_file(expanduser('~/www/website/static/fo-verify.html')), 200

@app.errorhandler(TooManyRequests)
def handle_rate_limit_exceeded(e):
    return jsonify({'tooManyRequests': 'the webserver is flooded with traffic. Try again, whenever you are ready...' }), 429

@app.errorhandler(404)
def no_found(e):
    gk.report()
    xsearch = xSearchForm()
    return render_template('404.html', xsearch=xsearch), 404

@views.route('/.well-known/apple-developer-merchantid-domain-association', methods=['GET'])
def apple_deveoper_merch():
    return send_file(expanduser('~/www/website/static/apple-developer-merchantid-domain-association')), 200

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
@gk.specific(rate_limit_rules=[{'count': 1, 'window': 60,"duration":2400}])
def well_known_trap():
    gk.report()
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
    gk.report()
    xsearch = xSearchForm()
    return render_template('index.html', xsearch=xsearch)


@views.route('/search.html', methods=['GET', 'POST'])
    xsearch = xSearchForm()
    if xsearch.validate_on_submit():
        filesearch = escape(xsearch.search.data)
        if len(filesearch) < 3 or len(filesearch) > 74:
            flash("Search terms must be at least 3 characters and a maximum of 75 characters")
            return render_template("search/search.html", xsearch=xsearch, search_results={}, found=False, error=True)
        else:
            search_results = {}
            search_results['rizon'] = {}
            search_results['rizon']['net'] = 'Rizon'
            search_results['rizon']["filename.xyz-MyProxyIPcom"] = {}
            search_results['rizon']["filename.xyz-MyProxyIPcom"]['desc'] = "filename.xyz-MyProxyIPcom"
            search_results['rizon']["filename.xyz-MyProxyIPcom"]['bots'] = {}
            search_results['rizon']["filename.xyz-MyProxyIPcom"]['bots']['xdccbot[01]'] = {}
            search_results['rizon']["filename.xyz-MyProxyIPcom"]['bots']['xdccbot[01]']['nick'] = 'XdccBot[01]'
            search_results['rizon']["filename.xyz-MyProxyIPcom"]['bots']['xdccbot[01]']['gets'] = '101x'
            search_results['rizon']["filename.xyz-MyProxyIPcom"]['bots']['xdccbot[01]']['pack'] = "#12"
            search_results['rizon']["filename.xyz-MyProxyIPcom"]['bots']['xdccbot[333]'] = {}
            search_results['rizon']["filename.xyz-MyProxyIPcom"]['bots']['xdccbot[333]']['nick'] = "XDccBot[333]"
            search_results['rizon']["filename.xyz-MyProxyIPcom"]['bots']['xdccbot[333]']['gets'] = "68x"
            search_results['rizon']["filename.xyz-MyProxyIPcom"]['bots']['xdccbot[333]']['pack'] = "#454"
    return render_template("search/search.html", xsearch=xsearch, search_results=search_results, found=True, error=False)

@views.route('/policy.html', methods=['GET'])
@views.route('/policy/', methods=['GET'])
def policy_wwww():
    gk.report()
    xsearch = xSearchForm()
    return render_template('policy.html', xsearch=xsearch)


@views.route('/hosted.html', methods=['GET'])
@views.route('/hosted/', methods=['GET'])
def hosted_info():
    gk.report()
    xsearch = xSearchForm()
    return render_template('hosted.html', xsearch=xsearch)


@views.route('/license/zero-bsd.html', methods=['GET'])
@views.route('/license/', methods=['GET'])
@views.route('/zero-bsd.html', methods=['GET'])
def zero_bsd():
    gk.report()
    xsearch = xSearchForm()
    return render_template('zero-bsd.html', xsearch=xsearch)


@views.route('/coc/code_of_conduct.html', methods=['GET'])
@views.route('/code_of_conduct.html', methods=['GET'])
@views.route('/coc/', methods=['GET'])
@views.route('/coc.html', methods=['GET'])
def coc():
    gk.report()
    xsearch = xSearchForm()
    return render_template('coc.html', xsearch=xsearch)


@views.route('/contributing/', methods=['GET'])
@views.route('/contrib/', methods=['GET'])
@views.route('/contributing.html', methods=['GET'])
@views.route('/contrib.html', methods=['GET'])
def contrib():
    gk.report()
    xsearch = xSearchForm()
    return render_template('contributing.html', xsearch=xsearch)

@views.route('/privacypolicy/', methods=['GET'])
@views.route('/policy/', methods=['GET'])
@views.route('/privacypolicy.html', methods=['GET'])
@views.route('/policy.html', methods=['GET'])
def policy():
    gk.report()
    xsearch = xSearchForm()
    return render_template('policy.html', xsearch=xsearch)

@views.route('/security.html', methods=['GET'])
@views.route('/security/', methods=['GET'])
def security():
    gk.report()
    xsearch = xSearchForm()
    return render_template('security.html', xsearch=xsearch)


@views.route('/download.html', methods=['GET'])
@views.route('/download/', methods=['GET'])
def download_msl():
    gk.report()
    xsearch = xSearchForm()
    return render_template('download.html', xsearch=xsearch)

