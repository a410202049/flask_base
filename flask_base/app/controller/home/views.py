from flask import render_template,current_app as app
from app.controller.home import home

@home.route('/', methods=['GET', 'POST'])
def index():
    app.logger.debug('xxx')
    return render_template('home/index.html')

@home.route('/sys-status/', methods=['GET', 'POST'])
def get_service_status():
    return 'I\'m still alive.<br>version %s' % (app.config['VERSION'])