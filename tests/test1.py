#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/29 下午6:57
# @Author  : KoKoa
# @File    : test1.py
# @Software: PyCharm

import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(chrome_options=chrome_options)

base_url = "http://www.baidu.com/"
# 对应的chromedriver的放置目录
driver = webdriver.Chrome(chrome_options=chrome_options)

driver.get(base_url + "/")

start_time = time.time()
print('this is start_time ', start_time)

driver.find_element_by_id("kw").send_keys("selenium webdriver")
driver.find_element_by_id("su").click()
driver.save_screenshot('screen.png')

driver.close()

end_time = time.time()
print('this is end_time ', end_time)
