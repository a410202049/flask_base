#!/usr/bin/python
# -*- encoding: utf-8 -*-
from axf_utils.context.context import Context


class CeleryContext(Context):
    def __init__(self, context=None, task_name=None):
        super(CeleryContext, self).__init__(context)

        if context and isinstance(context, CeleryContext):
            self.task_name = context.task_name
        else:
            self.task_name = task_name

        from celery_task.log import CeleryLog
        self.log = CeleryLog(self)
