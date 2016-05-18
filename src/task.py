#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'fdrong'
__mtime__ = '16/5/17'
"""

import time
import datetime
from src.base import BaseSpider
from src.config import SinaConfig
from celery.task import task
from celery.task import periodic_task
from celery.schedules import timedelta
from celery.schedules import crontab


# 测试celery的crontab定时任务和timedelta轮询任务
# @periodic_task(run_every=crontab(hour=11, minute=20))
# def test_crontab():
#     print(datetime.datetime.now())
#
#
# @periodic_task(run_every=timedelta(minutes=1))
# def test_timedelta():
#     print("hello timedelta: %s" % datetime.datetime.now())


@periodic_task(run_every=timedelta(minutes=5))
def spider_sina_news():
    start = time.time()
    spider = BaseSpider(config=SinaConfig)
    spider.run()
    end = time.time()
    print "spider sina news costs:%ds" % (end - start)