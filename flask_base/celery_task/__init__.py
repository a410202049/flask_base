#!/usr/bin/python
# -*- encoding: utf-8 -*-
from celery import Celery


celery = None


class Config:
    VERSION = '1.0.0'
    SYS_API_INST = None
    LOG_FOLDER = './logs'
    LOG_FILE_VALID_DAYS = 7
    CUSTOMER_LOG_VALID_DAYS = 15
    FEE_LOG_VALID_DATE = 60
    FEE_RECORD_LOG_VALID_DAYS = 60


def make_celery(app):
    global celery
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'], broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    Config.from_map(app.config)
    return celery

