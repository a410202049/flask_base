# -*- coding:utf-8 -*-
from app.controller.api_v1 import api_blueprint
from app.utils.restful_response import CommonResponse, ResultType
from flask import request,current_app as app,abort

@api_blueprint.route('/getUserInfo/<int:uid>', methods=['GET'])
def group_grant(uid):
    # abort(404)
    # try:
    # a = '0' / 12
    #     print a
    # except Exception as e:
    #     app.logger.info(e)
    return CommonResponse(ResultType.Success, message=u"获取成功",data="uid is {0}".format(uid)).to_json()
