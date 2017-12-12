#!/usr/bin/python
# -*- encoding: utf-8 -*-
from axf_utils.structed_log import BaseLog, LogType
from axf_utils.structed_log import get_log
from celery_task.context import CeleryContext


class CeleryLog(BaseLog):

    def __init__(self, celery_context):
        super(CeleryLog, self).__init__(celery_context)

        if not isinstance(celery_context, CeleryContext):
            raise RuntimeError('expect CeleryLog but got %s' % celery_context.__class__)

        self.gen_log = get_log('celery')
        # self.logger = get_log('celery')

    def get_header(self):
        return super(CeleryLog, self).get_header() + u'[task:%s]' % self.get_context().task_name

    def get_log_type(self):
        return LogType.AsyncTask
