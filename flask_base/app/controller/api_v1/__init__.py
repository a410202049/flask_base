# -*- coding:utf-8 -*-
from flask import Blueprint,request,current_app as app,jsonify
import traceback

api_blueprint = Blueprint('api', __name__,url_prefix='/api/v1.1.0')
from app.controller.api_v1 import UserService

@api_blueprint.before_request
def before_request():
    method = request.method
    header = request.headers.to_list()
    args = {
        'GET': request.args,
        'POST': request.form
    }[request.method]
    app.logger.info('\n[method]: {} \n'
                    '[headers]:\n {}\n'
                    '[args]:{}\n'.format(method,header,args.to_dict()))

@api_blueprint.after_request
def after_request(response):
    app.logger.info('\n[response] :\n {}\n'.format(response.data.replace('\n','').replace(' ','')))
    return response

@api_blueprint.errorhandler(Exception)
def code_exception_found(e):
    trace = traceback.format_exc()
    app.logger.info('\n[Exception] :\n {}\n'.format(trace))


@api_blueprint.errorhandler(404)
def page_not_found(e):
    response = jsonify({'error': 'not found','status':1})
    response.status_code = 404
    return response
