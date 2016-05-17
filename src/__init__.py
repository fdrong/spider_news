#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'fdrong'
__mtime__ = '16/5/16'
"""


from celery import Celery
from celery import platforms

app = Celery('spider_news', include=['src.task'])

app.config_from_object('src.config')

platforms.C_FORCE_ROOT = True  # 在ROOT下启动

if __name__ == '__main__':
    app.start()