#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/28 上午10:28
# @Author  : KoKoa
# @File    : celery.py
# @Software: PyCharm
from __future__ import absolute_import
from celery import Celery

celery = Celery('app', include=['app.tasks'])
celery.config_from_object('app.celery_config')
