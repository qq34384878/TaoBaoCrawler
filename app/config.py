#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/28 下午6:46
# @Author  : KoKoa
# @File    : config.py
# @Software: PyCharm

ORDER_HEADER = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.q=0.8,en;q=0.7',
    'content - length': '33',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'origin': 'https://buyertrade.taobao.com',
    'referer': 'https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

# WangCheng
# MONGO_URL = '193.112.75.62'
# 本地
MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
TAOBAO_COLLECTION = 'result'

QRCODE_COLLECTION = 'qrcode'

# Redis数据库地址
# REDIS_HOST = 'localhost'
REDIS_HOST = '192.168.2.182'

# Redis端口
REDIS_PORT = 6379

# Redis密码，如无填None
REDIS_PASSWORD = None

# 产生器使用的浏览器
BROWSER_TYPE = 'Firefox'

# 产生器类，如扩展其他站点，请在此配置
GENERATOR_MAP = {
    # 'weibo': 'WeiboCookiesGenerator'
    'taobao': 'TaoBaoCookiesGenerator'
}

# 测试类，如扩展其他站点，请在此配置
TESTER_MAP = {
    # 'weibo': 'WeiboValidTester'
    'taobao': 'TaoBaoValidTester'
}

TEST_URL_MAP = {
    # 'weibo': 'https://m.weibo.cn/'
    'taobao': 'https://www.taobao.com/'
}

# 产生器和验证器循环周期
CYCLE = 120

# API地址和端口
API_HOST = '0.0.0.0'
API_PORT = 5000

# 产生器开关，模拟登录添加Cookies
GENERATOR_PROCESS = False
# 验证器开关，循环检测数据库中Cookies是否可用，不可用删除
VALID_PROCESS = False
# API接口服务
API_PROCESS = True
