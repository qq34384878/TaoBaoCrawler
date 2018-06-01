#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/28 上午10:27
# @Author  : KoKoa
# @File    : tasks.py
# @Software: PyCharm

# coding:utf-8
import uuid

import requests

from app import create_app
from flask_mail import Mail
from app.celery import celery
import random, time

from app.db import RedisClient
from app.spider import Browser, cookies2cookie, get_comment, get_collect, get_order, guess_you_like, get_info, get_user


# 任何需要作为后台任务的函数都需要使用 celery.task 装饰器装饰

@celery.task
def add(x=0, y=0):
    """
    celery队列测试
    :param x:
    :param y:
    :return:
    """
    return x + y


@celery.task
def req(url="http://httpbin.org/ip"):
    """
    celery请求测试
    :param url:
    :return:
    """
    res = requests.get(url)
    return res


@celery.task
def async_send_email(msg):
    """
    邮件发送任务
    :param msg:
    :return:
    """
    # 注意：Flask-Mail 需要在应用的上下文中运行，因此在调用 send() 之前需要创建一个应用上下文
    app = create_app()
    with app.app_context():
        # 此异步调用返回值并不保留，因此应用本身无法知道是否调用成功或者失败。运行这个示例的时候，需要检查 Celery worker 的输出来排查发送邮件过程是否有问题
        Mail(app).send(msg)


@celery.task(bind=True)
def long_task(self):
    total = random.randint(10, 50)
    for i in range(total):
        # 自定义状态 state
        self.update_state(state=u'处理中', meta={'current': i, 'total': total})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'result': u'完成'}


@celery.task
def browser():
    driver = Browser()
    qrcode = driver.create_qrcode()
    conn = RedisClient('taobao', 'qrcode')
    id = uuid.uuid1().hex
    response = {
        'uuid': id,
        'qrcode': qrcode
    }
    conn.set(browser.request.id, response)
    driver.verify_login()
    if driver.login_signal == 1:
        cookie = driver.get_cookie()
        conn2 = RedisClient('taobao', 'cookie')
        conn2.set(id, cookie)
        celery.send_task('app.tasks.cookie_test', args=(id,))
        return True
    if driver.login_signal == 0:
        print('任务失败')
        return '任务失败'


@celery.task
def cookie_test(id):
    """
    cookie测试
    :return:
    """
    conn = RedisClient('taobao', 'cookie')
    cookies = conn.result(id)
    cookies = eval(cookies)
    cookie = cookies2cookie(cookies)
    user = get_user(cookie)
    comment = get_comment(cookie)
    info = get_info(cookie)
    colloct = get_collect(cookie)
    order = get_order(cookie)
    like = guess_you_like(cookie)
    data = {
        'id': user,
        '用户信息': info,
        '信誉明细': comment,
        '购物数据': order,
        '收藏信息': colloct,
        '猜你喜欢': like,
    }
    conn3 = RedisClient('taobao', 'result')
    conn3.set(user, data)
    return info
