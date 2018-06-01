#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/29 下午4:59
# @Author  : KoKoa
# @File    : tests.py
# @Software: PyCharm

from selenium import webdriver

chrome_options = webdriver.ChromeOptions()
# 使用headless无界面浏览器模式
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# 启动浏览器，获取网页源代码
browser = webdriver.Chrome(chrome_options=chrome_options)
mainUrl = "https://www.taobao.com/"
browser.get(mainUrl)
print(f"browser text = {browser.page_source}")
browser.quit()
