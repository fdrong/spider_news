# -*- coding: utf-8 -*-

# celery 配置信息
# CELERY_BROKER_URL = 'redis://localhost:6379/0'
BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_TIMEZONE = 'Asia/Shanghai'

