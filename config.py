# -*- coding:utf-8 -*-
__author__ = u'kerry'

import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = '\x03d\xf4\x95J\x15\xa4B\xfb\xc0\xaf \xd1A[j$}\x18\x16a\xe7\xd0\xec'
    STRIPE_API_KEY = '\x03d\xf4\x95J\x15\xa4B\xfb\xc0\xaf \xd1A[j$}\x18\x16a\xe7\xd0\xec'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    SQLALCHEMY_RECORD_QUERIES = True
    FLASKY_SLOW_DB_QUERY_TIME = 0.5
    WTF_CSRF_ENABLED = False
    PAGE_SIZE = 15
    SQLALCHEMY_ECHO = False
    MAX_CONTENT_LENGTH = 160 * 1024 * 1024
    ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
    VERSION = '1.0.1'
    DEBUG = True
    IS_LOCALHOST = True

    #邮件配置
    MAIL_SERVER = 'xxxxxxx'
    MAIL_USERNAME = 'xxxxxxx'
    MAIL_PASSWORD = 'xxxx'
    ADMINS_EMAIL = ['xxxxxxxxxxxxxxxx'] #发送给管理员

    #flask日志模块
    LOG_FILE = 'flask_record.log'
    LOG_LEVEL = 'd'
    LOG_FILE_MAX_SIZE = 10 * 1024 * 1024
    LOG_FILE_NUM_BACKUPS = 10

    #所有SQLALCHEMY配置项可参考手册http://www.pythondoc.com/flask-sqlalchemy/config.html#id2
    @staticmethod
    def init_app(app):
        pass


class LocalConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1/flask_base?charset=utf8"

    #CELERY
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
    CELERY_ENABLE_UTC = False
    CELERY_TIMEZONE = 'Asia/Shanghai'

    CELERY_INCLUDE = [
        'celery_task.push_message_task',
    ]

    CELERYBEAT_SCHEDULE = {
        'push_message_handler': {
            'task': 'celery_task.push_message_task.sync_push_message_task',
            'schedule': timedelta(seconds=60),
            'args': None
        }
    }

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1/flask_base?charset=utf8"

    #CELERY
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
    CELERY_ENABLE_UTC = False
    CELERY_TIMEZONE = 'Asia/Shanghai'

    CELERY_INCLUDE = [
        'celery_task.push_message_task',
    ]

    CELERYBEAT_SCHEDULE = {
        'push_message_handler': {
            'task': 'celery_task.push_message_task.sync_push_message_task',
            'schedule': timedelta(seconds=60),
            'args': None
        }
    }

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@127.0.0.1/flask_base?charset=utf8"

    #CELERY
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
    CELERY_ENABLE_UTC = False
    CELERY_TIMEZONE = 'Asia/Shanghai'

    CELERY_INCLUDE = [
        'celery_task.push_message_task',
    ]

    CELERYBEAT_SCHEDULE = {
        'push_message_handler': {
            'task': 'celery_task.push_message_task.sync_push_message_task',
            'schedule': timedelta(seconds=60),
            'args': None
        }
    }

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'local': LocalConfig,
}

