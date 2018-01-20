# coding: utf-8
from flask import current_app

from flask import render_template, flash, redirect, request, url_for
from flask_login import login_user, logout_user, login_required, current_user

from app.controller.admin import admin
from app.forms.forms import LoginForm
from app.models.models import User
from app.helpers.common_helper import record_log


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if current_app.config.get('IS_LOCALHOST'):
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is not None and user.verify_password(form.password.data):
                if not user.status:
                    #禁止被禁用的用户登陆
                    flash(u'用户被禁用，请联系管理员')
                else:
                    login_user(user, form.remember_me.data)
                    record_log('login', u'用户登陆', 'current_user:{username}'.format(username=current_user.username))
                    return redirect(request.args.get('next') or url_for('admin.index'))
            else:
                flash(u'用户名或密码错误')
        if current_user.is_authenticated:
            return redirect(url_for('admin.index'))
        return render_template('admin/login.html', form=form)
    else:
        return redirect(current_app.config.get('OPERATOR_LOGIN'))


@admin.route('/logout')
@login_required
def logout():
    record_log('logout', u'用户登出', 'current_user:{username}'.format(username=current_user.username))
    logout_user()
    # flash(u'您已经成功退出')
    if current_app.config.get('IS_LOCALHOST'):
        return redirect(url_for('admin.login'))
    else:
        return redirect(current_app.config.get('OPERATOR_LOGIN'))




