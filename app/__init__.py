# coding: utf-8
from flask import Flask,current_app
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy, get_debug_queries, BaseQuery
from flask_login import LoginManager

from app.utils.restful_response import CommonResponse, ResultType
from config import config
import datetime
from flask import render_template, request, jsonify

import time
from app.utils.log import FinalLogger

from celery_task import make_celery
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

mail = Mail()

#设置db.session.query 可以使用分页类
session_options = {}
session_options['query_cls'] = BaseQuery
db = SQLAlchemy(session_options=session_options)

login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'admin.login'
login_manager.login_message = None
VERSION = '1.0.0'

def register_blueprints(app):
    #注册蓝图
    from .controller.home import home
    app.register_blueprint(home)

    from .controller.admin import admin
    app.register_blueprint(admin)

    from .controller.api_v1 import api_blueprint
    app.register_blueprint(api_blueprint)

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    app.config['MAX_CONTENT_LENGTH'] = app.config.get('MAX_CONTENT_LENGTH')
    #开启调试模式
    app.debug = app.config.get('DEBUG')

    # #配置log路径
    log_handler = FinalLogger(app).getLogger()
    app.logger.addHandler(log_handler)
    #初始化celery
    # celery = make_celery(app)
    # app.celery = celery

    #注册蓝图
    register_blueprints(app)

    #添加当前时间戳 全局变量
    app.add_template_global(int(time.time()), 'current_time')

    @app.after_request
    def after_request(response):
        for query in get_debug_queries():
            if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
                current_app.logger.warning(
                    'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                    % (query.statement, query.parameters, query.duration,
                       query.context))
        return response

    @app.errorhandler(403)
    def forbidden(e):
        if request.accept_mimetypes.accept_json and \
                not request.accept_mimetypes.accept_html:
            response = jsonify({'error': 'forbidden'})
            response.status_code = 403
            return response
        return render_template('403.html'), 403


    @app.errorhandler(404)
    def page_not_found(e):
        if request.accept_mimetypes.accept_json and \
                not request.accept_mimetypes.accept_html:
            response = jsonify({'error': 'not found'})
            response.status_code = 404
            return response
        return render_template('404.html'), 404


    @app.errorhandler(500)
    def internal_server_error(e):
        if request.accept_mimetypes.accept_json and \
                not request.accept_mimetypes.accept_html:
            response = jsonify({'error': 'internal server error'})
            response.status_code = 500
            return response
        return render_template('500.html'), 500

    @app.template_filter("omit")
    def omit(data, length):
        if len(data) > length:
            return data[:length-3] + '...'
        return data

    @app.template_filter("friendly_time")
    def friendly_time(date):
        delta = datetime.datetime.now() - date
        if delta.days >= 365:
            return u'%d年前' % (delta.days / 365)
        elif delta.days >= 30:
            return u'%d个月前' % (delta.days / 30)
        elif delta.days > 0:
            return u'%d天前' % delta.days
        elif delta.seconds < 60:
            return u"%d秒前" % delta.seconds
        elif delta.seconds < 60 * 60:
            return u"%d分钟前" % (delta.seconds / 60)
        else:
            return u"%d小时前" % (delta.seconds / 60 / 60)
    return app


