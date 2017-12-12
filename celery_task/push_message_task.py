#!usr/bin/python
# -*- encoding: utf-8 -*-
from celery_task import celery, Config
from celery_task.context import CeleryContext
from app.models.device import Message,MessageStatus,BindDevice
from app.models.pay_records import PayRecords
from datetime import datetime,timedelta
from axf_system_api.message_system_api.message_system_api import MessageSystemApi
import json
from app import db

@celery.task()
def sync_push_message_task():
    context = CeleryContext(None, 'sync_push_message_task')
    context.log.d('start sync_push_message_task')
    messages = Message.query.order_by(Message.create_time.desc()).filter(
        Message.status != MessageStatus.PUSH_SUCCESS.value
        , Message.create_time > (datetime.utcnow() - timedelta(hours=1))).all()
    for msg in messages:
        device = db.session.query(BindDevice).filter(BindDevice.imei == msg.imei,BindDevice.is_valid==1).scalar()
        order = db.session.query(PayRecords).filter(PayRecords.order_no == msg.order_no).scalar()
        if device:
            message_system = MessageSystemApi(context)
            content = {}
            content['id'] = msg.id
            content['title'] = msg.title
            content['pay_addr'] = order.pay_address
            content['order_no'] = order.order_no
            content['amt'] = str(order.pay_amount)
            content['order_status'] = order.order_status
            content['pay_time'] = str(order.pay_time)
            content['pay_remark'] = order.pay_remark
            content['cashier_no'] = order.cashier_no
            content['pay_channel'] = order.pay_channel
            content['contains_refund'] = order.contains_refund
            data = message_system.send_message_by_gt(
                push_content=json.dumps({
                    "type": 'notify_message',
                    "title": content
                }), aims=device.client_id)

            context.log.d(data)
            if data['code'] == '20002':
                msg.status = MessageStatus.PUSH_FAIL.value
            elif data['code'] == '20001':
                msg.status = MessageStatus.PUSH_SUCCESS.value
            msg.push_times+=1
        db.session.merge(msg)
    db.session.commit()
