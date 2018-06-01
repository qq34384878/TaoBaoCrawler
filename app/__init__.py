#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/28 上午10:27
# @Author  : KoKoa
# @File    : __init__.py.py
# @Software: PyCharm

from flask import Flask


def create_app():
    app = Flask(__name__)
    # 随机字符串
    app.config['SECRET_KEY'] = 'LvMkE65cTnS1r2vbLE6tGk1TXSShaDBo'
    # Flask-Mail 配置
    app.config['MAIL_SERVER'] = 'smtp.163.com'  # 电子邮件服务器的主机名或IP地址
    app.config['MAIL_PORT'] = 25  # 电子邮件服务器的端口
    app.config['MAIL_USE_TLS'] = True  # 启用传输层安全协议
    app.config['MAIL_USE_SSL'] = False  # 启用安全套接层协议
    app.config['MAIL_USERNAME'] = 'fangyu_wh@163.com'  # 邮件账户用户名
    app.config['MAIL_PASSWORD'] = 'qqfy326498'  # 邮件账户的密码
    return app