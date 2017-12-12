# -*- coding:utf-8 -*-
from enum import unique, Enum

from app import db
from datetime import datetime
from sqlalchemy import DATETIME
from sqlalchemy import Column

@unique
class SchoolChannel2YMTChannel(Enum):
    UnionPay = "UnionPay"
    WxPay = "WxAppPay"
    AliPay = "AliAppPay"

#订单记录列表
class PayRecords(db.Model):
    __tablename__ = 't_pay_records'
    id = db.Column(db.Integer, primary_key=True)
    order_no = db.Column(db.String(32),doc=u'订单编号',nullable=False,unique=True)
    cashier_no = db.Column(db.String(32),doc=u'收银员编号',index=True)
    pay_amount  = db.Column(db.DECIMAL(12,2),doc=u"支付金额")
    stu_name = db.Column(db.String(24),doc=u'学生姓名')
    stu_no = db.Column(db.String(32),doc=u'学生编号')
    mobile = db.Column(db.String(11),doc=u'手机号')
    pay_address = db.Column(db.String(32),doc=u'支付地点')
    # order_type = db.Column(db.Integer,default=0,doc=u'订单类型 0-支付订单，1-退款订单')
    order_status = db.Column(db.Integer,default=0,doc=u'0支付成功 1退款成功 2退款失败')
    pay_time = Column("pay_time", DATETIME, nullable=False,doc=u'支付时间')
    pay_remark = db.Column(db.String(128), doc=u'支付备注')
    pay_channel = db.Column(db.String(32), doc=u'支付渠道')
    contains_refund = db.Column(db.Integer, doc=u'是否支持退款 1不支持 0支持')
    create_time = Column("create_time", DATETIME, nullable=False, default=datetime.now, doc=u'创建时间')
    update_time = Column("update_time", DATETIME, nullable=False, default=datetime.now, onupdate=datetime.now, doc=u'更新时间')
    remark = db.Column(db.String(128), doc=u'备注')

    def to_json(self):
        return {
            "id": self.id,
            "order_no": self.order_no,
            "cashier_no":self.cashier_no,
            "pay_amount": str(self.pay_amount),
            "stu_name":self.stu_name,
            "stu_no":self.stu_no,
            "mobile":self.mobile,
            "pay_address":self.pay_address,
            "pay_remark":self.pay_remark,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S") if self.create_time else '',
            "remark": self.remark
        }

    def __repr__(self):
        return '<PayRecords>\n' + '\n'.join(['%s:%s' % item for item in self.__dict__.items()])

