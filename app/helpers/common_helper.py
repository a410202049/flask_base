#!/usr/bin/python
# -*- encoding: utf-8 -*-
import datetime
from flask import request
from app.models.models import OperationLog
from app import db
from flask_login import current_user

#生成日期列表
def dateRange(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in xrange(0, days+1, step)]

#记录操作日志
def record_log(operation,desc = None,data=None):
    op = OperationLog()
    request_data = {}
    op.username = current_user.username
    op.operation = operation
    op.operate_desc = desc
    op.login_ip = request.remote_addr
    request_data.update(request.args)
    request_data.update(request.form)
    op.request  = str(request_data)
    op.response = str(data)
    db.session.merge(op)
    db.session.commit()

def tree(data,pid=0,pidName = 'pid',childName='child'):
    trees = []
    for da in data:
        if da[pidName] == pid:
            tmp = tree(data,da['id'],pidName,childName)
            if tmp:
                da[childName] = tmp
            trees.append(da)
    return trees

def fragment():
    gets = request.args
    #分页带条件
    fragment = ""
    for k in gets:
        if k == 'page':
            continue
        fragment+="&"+k+"="+gets[k]
    return fragment
