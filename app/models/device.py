# -*- coding:utf-8 -*-
from app import db
from datetime import datetime
from sqlalchemy import DATETIME
from sqlalchemy import Column
from enum import unique, Enum

@unique
class OnlineStatus(Enum):
    ONLINE = 1
    OFFLINE = 0

#绑定设备列表
class BindDevice(db.Model):
    __tablename__ = 't_bind_device'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(32),doc=u'品牌',nullable=False)
    model = db.Column(db.String(32),doc=u'型号',nullable=False)
    imei = db.Column(db.String(64),doc=u'国际移动设备识别码',unique=True)
    meid = db.Column(db.String(64),doc=u'移动设备识别码移动设备识别码')
    cashier_no = db.Column(db.String(32),doc=u'收银员编号',index=True)
    client_id = db.Column(db.String(32),doc=u'个推唯一标识')
    online_status = db.Column(db.Integer,default=1,doc=u"0 OFFLINE,1 ONLINE")
    is_valid  = db.Column(db.Integer,default=1,doc=u"是否生效 0失效 1生效")
    merch_id = db.Column(db.String(32),doc=u'商户id')
    qr_id = db.Column(db.String(32), doc=u'二维码id')
    create_time = Column("create_time", DATETIME, nullable=False, default=datetime.now, doc=u'创建时间')
    update_time = Column("update_time", DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now, doc=u'更新时间')
    remark = db.Column(db.String(128), doc=u'备注')

    # __table_args__ = (
    #     db.UniqueConstraint('imei', 'client_id', name='uix_imei_client_id'),
    # )

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "imei": self.imei,
            "meid": self.meid,
            "cashier_no":self.cashier_no,
            "client_id": self.client_id,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time else '',
            "remark": self.remark
        }

    def __repr__(self):
        return '<BindDevice>\n' + '\n'.join(['%s:%s' % item for item in self.__dict__.items()])


#绑定设备记录
class BindDeviceRecords(db.Model):
    __tablename__ = 't_device_records'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(32),doc=u'品牌',nullable=False)
    model = db.Column(db.String(32),doc=u'型号',nullable=False)
    imei = db.Column(db.String(64),doc=u'国际移动设备识别码')
    meid = db.Column(db.String(64),doc=u'移动设备识别码移动设备识别码')
    cashier_no = db.Column(db.String(32),doc=u'收银员编号')
    client_id = db.Column(db.String(32),doc=u'个推唯一标识')
    merch_id = db.Column(db.String(32),doc=u'商户id')
    qr_id = db.Column(db.String(32), doc=u'二维码id')
    create_time = Column("create_time", DATETIME, nullable=False, default=datetime.now, doc=u'创建时间')
    update_time = Column("update_time", DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now, doc=u'更新时间')
    remark = db.Column(db.String(128), doc=u'备注')

    # __table_args__ = (
    #     db.UniqueConstraint('imei', 'client_id', name='uix_imei_client_id'),
    # )

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "imei": self.imei,
            "meid": self.meid,
            "cashier_no":self.cashier_no,
            "client_id": self.client_id,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time else '',
            "remark": self.remark
        }

    def __repr__(self):
        return '<BindDeviceRecords>\n' + '\n'.join(['%s:%s' % item for item in self.__dict__.items()])


@unique
class MessageStatus(Enum):
    NOTPUSH = 0
    PUSH_SUCCESS = 1
    PUSH_FAIL = 2

#设备消息
class Message(db.Model):
    __tablename__ = 't_message'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32),doc=u'标题',nullable=False)
    content = db.Column(db.String(32),doc=u'推送内容',nullable=False)
    status = db.Column(db.Integer,doc=u'推送状态 0- 未推送 1- 推送成功 2- 推送失败',default=0)
    push_times = db.Column(db.Integer,doc=u'推送次数',default=0)
    cashier_no = db.Column(db.String(32),doc=u'收银员编号',index=True)
    order_no = db.Column(db.String(32),doc=u'订单编号')
    imei = db.Column(db.String(64),doc=u'国际移动设备识别码')
    create_time = Column("create_time", DATETIME, nullable=False, default=datetime.now, doc=u'创建时间')
    update_time = Column("update_time", DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now, doc=u'更新时间')
    remark = db.Column(db.String(128), doc=u'备注')

    # __table_args__ = (
    #     db.UniqueConstraint('imei', 'meid', name='uix_imei_meid'),
    # )

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "status": self.status,
            "push_times":self.push_times,
            "cashier_no": self.cashier_no,
            "order_no":self.order_no,
            "imei":self.imei,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time else '',
            "remark": self.remark
        }

    def __repr__(self):
        return '<Message>\n' + '\n'.join(['%s:%s' % item for item in self.__dict__.items()])
