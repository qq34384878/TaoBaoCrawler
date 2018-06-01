#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/28 上午10:28
# @Author  : KoKoa
# @File    : celery_config.py
# @Software: PyCharm

# 使用 Redis 作为消息代理
# BROKER_URL = 'redis://localhost:6379/15'
BROKER_URL = 'redis://192.168.2.182:6379/15'
# 把任务结果存在 Redis
# CELERY_RESULT_BACKEND = 'redis://localhost:6379/15'
CELERY_RESULT_BACKEND = 'redis://192.168.2.182:6379/15'
