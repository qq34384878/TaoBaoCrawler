#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/28 上午11:41
# @Author  : KoKoa
# @File    : utils.py
# @Software: PyCharm
import datetime
import re
import time

from lxml import etree


def page2html(page):
    """
    doc转HTML
    :param page:
    :return:
    """
    html = etree.HTML(page)
    return html


def verify_re_content(pattern, html):
    """
    Re正则结果验证
    :param pattern:
    :param html:
    :return:
    """
    result = re.search(pattern, html, re.S)
    if result:
        return True
    else:
        return False


def calculating_time(date):
    """
    时间转换为天
    :param date:
    :return:
    """
    now = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    d1 = datetime.datetime.strptime(date, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(now, '%Y-%m-%d')
    delta = d2 - d1
    return delta.days
