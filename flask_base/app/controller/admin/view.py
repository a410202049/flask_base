#!/usr/bin/python
# -*- encoding: utf-8 -*-

from app.controller.admin import admin
from flask import render_template, request, current_app as app, json
from flask_login import login_required, current_user

from app.forms.forms import MenuForm, UserForm
from app.helpers.common_helper import record_log
from app import db
from app.utils.restful_response import CommonResponse, ResultType
from app.models.models import MenuAuth,User,UsersGroup
from app.utils.auth import Auth
from app.helpers.common_helper import tree,fragment


#后台首页
@admin.route('/', methods=['GET', 'POST'])
@admin.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    data = {}
    #累加
    # db.session.query(PackageUser).filter(PackageUser.id == 5).update({"share_num": PackageUser.share_num + 1})
    # db.session.commit()
    return render_template('admin/index.html',data=data)

#菜单查询
@admin.route('/menu-auth', methods=['GET', 'POST'])
@login_required
def menu_auth():
    menus = MenuAuth.query.order_by('id').all()
    auth = Auth()
    menus = auth.tree_list(menus)
    return render_template('admin/menu_auth.html',data=menus)

#获取菜单信息
@admin.route('/get-menu-info', methods=['GET', 'POST'])
@login_required
def get_menu_info():
    menu_id = request.form.get('menu_id')
    if not menu_id:
        return CommonResponse(ResultType.Failed, message=u"menu_id为空").to_json()
    menu_info_obj = MenuAuth.query.filter(MenuAuth.id == menu_id).scalar()
    if menu_info_obj is None:
        return CommonResponse(ResultType.Failed, message=u"菜单不存在").to_json()
    menu_info = menu_info_obj.to_json()
    return CommonResponse(ResultType.Success, message=u"获取成功",data=menu_info).to_json()

#添加菜单
@admin.route('/menu-add', methods=['GET', 'POST'])
@login_required
def menu_add():
    form = MenuForm()
    try:
        if not form.validate():
            error_message = form.get_error()
            return CommonResponse(ResultType.Failed, message=error_message).to_json()
        else:
            menu = MenuAuth()
            menu.name = form.menu_name.data
            menu.method = form.method.data
            menu.type = form.type.data
            menu.icon = form.icon.data
            menu.sort = form.sort.data
            menu.parent_id = form.parent_id.data
            db.session.merge(menu)
            db.session.commit()
            record_log('add_menu', u'添加菜单',u'method:{method}'.format(method=form.method.data))
            return CommonResponse(ResultType.Success, message=u"添加成功").to_json()
    except Exception, e:
        db.session.rollback()
        record_log('add_menu', u'添加菜单失败')
        return CommonResponse(ResultType.Failed, message=u"添加失败").to_json()


#编辑菜单
@admin.route('/menu-edit', methods=['GET', 'POST'])
@login_required
def menu_edit():
    form = MenuForm()
    try:
        if not form.validate():
            error_message = form.get_error()
            return CommonResponse(ResultType.Failed, message=error_message).to_json()
        else:
            menu = MenuAuth()
            menu.id = form.id.data
            menu.name = form.menu_name.data
            menu.method = form.method.data
            menu.type = form.type.data
            menu.icon = form.icon.data
            menu.sort = form.sort.data
            menu.parent_id = form.parent_id.data
            db.session.merge(menu)
            db.session.commit()
            record_log('add_menu', u'编辑菜单',u'method:{method}'.format(method=form.method.data))
            return CommonResponse(ResultType.Success, message=u"编辑成功").to_json()
    except Exception, e:
        db.session.rollback()
        record_log('add_menu', u'编辑菜单失败')
        return CommonResponse(ResultType.Failed, message=u"编辑失败").to_json()

# 删除菜单
@admin.route('/menu-del', methods=['GET', 'POST'])
@login_required
def menu_del():
    menu_id = request.form.get('menu_id')
    if not menu_id:
        return CommonResponse(ResultType.Failed, message=u"menu_id不能为空").to_json()
    menu_info_obj = MenuAuth.query.filter(MenuAuth.id == menu_id).scalar()
    if menu_info_obj is None:
        return CommonResponse(ResultType.Failed, message=u"菜单不存在").to_json()
    other_info_obj = MenuAuth.query.filter(MenuAuth.parent_id == menu_id).all()
    if other_info_obj:
        return CommonResponse(ResultType.Failed, message=u"删除菜单前，请先删除子菜单").to_json()

    record_log('del_menu', u'删除菜单', 'name:{name}'.format(name=menu_info_obj.name))
    db.session.delete(menu_info_obj)
    db.session.commit()
    return CommonResponse(ResultType.Success, message=u"删除成功").to_json()


#用户管理
@admin.route('/user-manage', methods=['GET', 'POST'])
@login_required
def user_manage():

    username = request.args.get('username', '')
    email = request.args.get('email', '')
    page = request.args.get('page', 1, type=int)
    user_obj = User.query.order_by(User.create_time.desc())
    if username !='':
        user_obj = user_obj.filter(User.username == username)
    if email !='':
        user_obj = user_obj.filter(User.email == email)



    paginate = user_obj.paginate(
        page, per_page=app.config['PAGE_SIZE'], error_out=True)
    users = paginate.items

    user_grops = db.session.query(UsersGroup).all()
    data = {
        "email":email,
        "username":username,
        "users":users,
        "pagination":paginate,
        "fragment":fragment(),
        "user_grops":user_grops
    }

    return render_template('admin/user_manage.html',data=data)

#添加用户
@admin.route('/user-add', methods=['GET', 'POST'])
@login_required
def user_add():
    form = UserForm()
    try:
        if not form.validate():
            error_message = form.get_error()
            return CommonResponse(ResultType.Failed, message=error_message).to_json()
        else:
            user = User()
            user.username = form.username.data
            user.password = form.password.data
            user.email = form.email.data
            if form.group_id.data:
                user.group_id = form.group_id.data
                user.is_manage = '1'
            db.session.add(user)
            db.session.commit()
            record_log('add_user', u'添加用户',u'username:{username}'.format(username=form.username.data))
            return CommonResponse(ResultType.Success, message=u"添加成功").to_json()
    except Exception, e:
        db.session.rollback()
        record_log('add_user', u'添加用户失败')
        return CommonResponse(ResultType.Failed, message=u"添加失败").to_json()

#获取菜单信息
@admin.route('/get-user-info', methods=['GET', 'POST'])
@login_required
def get_user_info():
    user_id = request.form.get('user_id')
    if not user_id:
        return CommonResponse(ResultType.Failed, message=u"user_id不能为空").to_json()
    user_info_obj = User.query.filter(User.id == user_id).scalar()
    if user_info_obj is None:
        return CommonResponse(ResultType.Failed, message=u"用户不存在").to_json()
    user_info = user_info_obj.to_json()
    return CommonResponse(ResultType.Success, message=u"获取成功",data=user_info).to_json()

#编辑用户
@admin.route('/user-edit', methods=['GET', 'POST'])
@login_required
def user_edit():
    form = UserForm()
    try:
        if not form.validate():
            error_message = form.get_error()
            return CommonResponse(ResultType.Failed, message=error_message).to_json()
        else:
            user = User()
            user.id = form.id.data
            user.username = form.username.data
            if form.password.data:
                user.password = form.password.data
            user.email = form.email.data
            if form.group_id.data:
                user.group_id = form.group_id.data
                user.is_manage = '1'
            else:
                user.group_id = None
                user.is_manage = '0'

            db.session.merge(user)
            db.session.commit()
            record_log('edit_user', u'编辑用户',u'username:{username}'.format(username=form.username.data))
            return CommonResponse(ResultType.Success, message=u"编辑成功").to_json()
    except Exception, e:
        db.session.rollback()
        record_log('edit_user', u'编辑用户失败')
        return CommonResponse(ResultType.Failed, message=u"编辑失败").to_json()

# 删除用户
@admin.route('/user-del', methods=['GET', 'POST'])
@login_required
def user_del():
    user_id = request.form.get('user_id')
    if int(current_user.id) == int(user_id):
        return CommonResponse(ResultType.Failed, message=u"不能删除自己的账号").to_json()

    if user_id is None:
        return CommonResponse(ResultType.Failed, message=u"user_id不能为空").to_json()
    user_info_obj = User.query.filter(User.id == user_id).scalar()
    if user_info_obj is None:
        return CommonResponse(ResultType.Failed, message=u"用户不存在").to_json()

    record_log('del_user', u'删除用户', 'name:{name}'.format(name=user_info_obj.username))
    db.session.delete(user_info_obj)
    db.session.commit()
    return CommonResponse(ResultType.Success, message=u"删除成功").to_json()


#用户组管理
@admin.route('/user-group-manage', methods=['GET', 'POST'])
@login_required
def user_group_manage():

    name = request.args.get('name', '')
    status = request.args.get('status', '')

    page = request.args.get('page', 1, type=int)
    user_group_obj = UsersGroup.query.order_by(UsersGroup.create_time.desc())

    if name !='':
        user_group_obj = user_group_obj.filter(UsersGroup.name == name)
    if status !='' and status !='ALL':
        user_group_obj = user_group_obj.filter(UsersGroup.status == status)


    paginate = user_group_obj.paginate(
        page, per_page=app.config['PAGE_SIZE'], error_out=True)
    groups = paginate.items

    data = {
        "name":name,
        "status":status,
        "pagination":paginate,
        "fragment":fragment(),
        "groups":groups
    }

    return render_template('admin/group_manage.html',data=data)


#添加分组
@admin.route('/group-add', methods=['GET', 'POST'])
@login_required
def group_add():
    try:
        name = request.form.get('name')
        status = request.form.get('status',default=1)
        if not name:
            return CommonResponse(ResultType.Failed, message=u"分组名称不能为空").to_json()
        user_group_obj = db.session.query(UsersGroup).filter(UsersGroup.name == name).scalar()
        if user_group_obj:
            return CommonResponse(ResultType.Failed, message=u"分组名称不能重复").to_json()
        group = UsersGroup()
        group.name = name
        group.status = status
        db.session.merge(group)
        db.session.commit()

        record_log('add_group', u'添加分组',u'name:{name}'.format(name=name))
        return CommonResponse(ResultType.Success, message=u"添加成功").to_json()
    except Exception, e:
        db.session.rollback()
        record_log('add_user', u'添加用户失败')
        return CommonResponse(ResultType.Failed, message=u"添加失败").to_json()

# 编辑分组
@admin.route('/group-edit', methods=['GET', 'POST'])
@login_required
def group_edit():
    try:
        id = request.form.get('id')
        name = request.form.get('name')
        status = request.form.get('status', default=1)
        if not name:
            return CommonResponse(ResultType.Failed, message=u"分组名称不能为空").to_json()
        user_group_obj = db.session.query(UsersGroup).filter(UsersGroup.id != id,UsersGroup.name == name).scalar()
        if user_group_obj:
            return CommonResponse(ResultType.Failed, message=u"分组名称不能重复").to_json()
        group = UsersGroup()
        group.id = id
        group.name = name
        group.status = status
        db.session.merge(group)
        db.session.commit()

        record_log('edit_group', u'编辑分组', u'name:{name}'.format(name=name))
        return CommonResponse(ResultType.Success, message=u"编辑成功").to_json()
    except Exception, e:
        db.session.rollback()
        record_log('add_user', u'编辑用户失败')
    return CommonResponse(ResultType.Failed, message=u"编辑失败").to_json()



#获取分组权限
@admin.route('/get-rule-list', methods=['GET', 'POST'])
@login_required
def get_rule_list():
    group_id = request.form.get('group_id')
    menus = db.session.query(MenuAuth).all()
    groups_obj = db.session.query(UsersGroup).filter(UsersGroup.id == group_id).scalar()
    rules_str = groups_obj.rules
    user_rules = []
    if rules_str:
        user_rules = json.loads(rules_str)
    if user_rules:
        for index, menu in enumerate(menus):
            for rule in user_rules:
                if rule == menu.id:
                    menus[index].active = True
                    break
                menus[index].active = False
    else:
        for index,menu in enumerate(menus):
            menus[index].active = False
    data = []
    for menu in menus:
        da = {}
        da['id'] = menu.id
        da['active'] = menu.active
        da['name'] = menu.name
        da['parent_id'] = menu.parent_id
        data.append(da)
    ret = tree(data,pidName='parent_id')
    return CommonResponse(ResultType.Success, message=u"获取成功",data=ret).to_json()

#获取分组信息
@admin.route('/get-group-info', methods=['GET', 'POST'])
@login_required
def get_group_info():
    group_id = request.form.get('group_id')
    if not group_id:
        return CommonResponse(ResultType.Failed, message=u"group_id不能为空").to_json()
    group_info_obj = UsersGroup.query.filter(UsersGroup.id == group_id).scalar()
    if group_info_obj is None:
        return CommonResponse(ResultType.Failed, message=u"分组不存在").to_json()
    group_info = group_info_obj.to_json()
    return CommonResponse(ResultType.Success, message=u"获取成功",data=group_info).to_json()

# 删除分组
@admin.route('/group-del', methods=['GET', 'POST'])
@login_required
def group_del():
    group_id = request.form.get('group_id')
    user_group_obj = db.session.query(UsersGroup).filter(UsersGroup.id == group_id).scalar()
    if user_group_obj is None:
        return CommonResponse(ResultType.Failed, message=u"分组不存在").to_json()
    user_obj = db.session.query(User).filter(User.group_id == group_id).all()
    if user_obj:
        return CommonResponse(ResultType.Failed, message=u"请先移除当前分组下的用户").to_json()

    record_log('del_group', u'删除分组', 'name:{name}'.format(name=user_group_obj.name))
    db.session.delete(user_group_obj)
    db.session.commit()
    return CommonResponse(ResultType.Success, message=u"删除成功").to_json()

#授权
@admin.route('/group_grant', methods=['GET', 'POST'])
@login_required
def group_grant():
    try:
        group_id = request.form.get('group_id')
        rules = request.form.get('rules')
        # rules = json.loads(rules_str)
        user_group_obj = db.session.query(UsersGroup).filter(UsersGroup.id == group_id).scalar()
        user_group_obj.rules = rules
        db.session.merge(user_group_obj)
        db.session.commit()
        record_log('group_grant', u'分组授权', 'name:{name}'.format(name=user_group_obj.name))
        return CommonResponse(ResultType.Success, message=u"授权成功").to_json()
    except Exception, e:
        db.session.rollback()
        record_log('group_grant', u'分组授权失败')
    return CommonResponse(ResultType.Failed, message=u"授权失败").to_json()



