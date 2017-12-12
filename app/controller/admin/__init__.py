# -*- coding:utf-8 -*-
from flask import Blueprint, request, json

from app.models.models import MenuAuth
from app.utils.auth import Auth
from flask_login import current_user
from app.utils.restful_response import CommonResponse, ResultType

admin = Blueprint('admin', __name__,url_prefix='/admin')
from app.controller.admin import auth,view

@admin.context_processor
def menus():
    user = current_user
    #获取登陆后菜单
    if user.is_active == True:
        #设置admin蓝图下全局变量
        auth= Auth(user)
        menus= auth.auth_menus()
        return {'menus': menus}
    return {}

#权限验证
@admin.before_request
def before_request():
    user = current_user
    path = request.path[1:]
    path = path + 'index' if path == 'admin/' else path
    if user.is_active == True:
        if user.group_id == 1:
            return
        all_menus = MenuAuth.query.order_by('id').all()
        rules_str = user.group.rules
        rules = []
        if rules_str :
            rules = json.loads(rules_str)
        all_menu_list = []
        auth_menu_list = []
        for menu in all_menus:
            all_menu_list.append(menu.method)
            for rule_id in rules:
                if int(menu.id) == rule_id:
                    auth_menu_list.append(menu.method)

        if path in all_menu_list and path not in auth_menu_list:
            return CommonResponse(ResultType.Failed, message=u"没有权限").to_json()
