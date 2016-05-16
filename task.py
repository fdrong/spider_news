# -*- coding: utf-8 -*-


import datetime

from celery.task import periodic_task
from celery.schedules import timedelta
from celery.schedules import crontab


# 测试celery的crontab定时任务和timedelta轮询任务
@periodic_task(run_every=crontab(hour=11, minute=20))
def test_crontab():
    print(datetime.datetime.now())


@periodic_task(run_every=timedelta(minutes=1))
def test_timedelta():
    print("hello timedelta: %s" % datetime.datetime.now())

