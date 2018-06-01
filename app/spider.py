#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/28 上午11:33
# @Author  : KoKoa
# @File    : spider.py
# @Software: PyCharm
import re
import time

import requests
from lxml import etree
from selenium import webdriver

from app.config import ORDER_HEADER
from app.utils import page2html, verify_re_content, calculating_time

# 用户信息
USERINFO_URL = 'https://member1.taobao.com/member/fresh/account_security.htm'

BASEINFO_URL = 'https://i.taobao.com/user/baseInfoSet.htm'


class Browser():
    def __init__(self):
        self.driver = webdriver.Firefox()
        # self.driver = webdriver.Chrome()
        # self.driver = webdriver.PhantomJS()
        # 登录信号
        self.login_signal = 0
        # 设置超时任务时间
        self.start_time = time.time()

    def create_qrcode(self):
        """
        生成一个二维码
        :return: 二维码图片地址
        """
        browser = self.driver
        browser.get('https://login.taobao.com/member/login.jhtml')
        html = page2html(browser.page_source)
        qrcode_img = html.xpath('//div[@id="J_QRCodeImg"]/img/@src')
        qrcode_img = 'https:' + qrcode_img[0]
        print(qrcode_img)
        return qrcode_img

    def verify_login(self):
        """
        判断是否登录成功
        :return:
        """
        if int(time.time() - self.start_time) >= 60:
            self.close()
            return '任务超时'
        if verify_re_content(r'待收货', self.driver.page_source):
            print('success')
            html = etree.HTML(self.driver.page_source)
            name = html.xpath('//*[contains(@class, "J_MemberNick")]/text()')
            if len(name) >= 1:
                self.login_signal = 1
                username = name[0]
                print(username)
                return username
        else:
            time.sleep(1)
            print('验证登录中')
            self.verify_login()

    def get_cookie(self):
        """
        获取Cookies
        :return:
        """
        cookies = self.driver.get_cookies()
        self.close()
        return cookies

    def close(self):
        return self.driver.close()


def test_cookie(cookie):
    """
    验证cookies
    :return:
    """
    pass


def cookies2cookie(cookies):
    """
    获取账号cookie
    :return: cookie
    """
    cookie = {}
    for item in cookies:
        cookie[item['name']] = item['value']
    print(cookie)
    return cookie


# 获取好中差评数
def get_comment(cookie):
    try:
        comment_url = 'https://rate.taobao.com/myRate.htm'
        resp = requests.get(url=comment_url, cookies=cookie)
        html = etree.HTML(resp.content)
        xinyong = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/h4[2]/a[1]/text()')
        comment = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/p/strong/text()')
        # 总计
        hao_num = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[1]/td[6]//text()')
        zhong_num = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[2]/td[6]//text()')
        cha_num = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[3]/td[6]//text()')
        sum = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[4]/td[6]//text()')
        # 最近1周
        hao_one_week = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[1]/td[2]//text()')
        zhong_one_week = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[2]/td[2]//text()')
        cha_one_week = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[3]/td[2]//text()')
        sum_one_week = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[4]/td[2]//text()')
        # 最近1个月
        hao_one_month = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[1]/td[3]//text()')
        zhong_one_month = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[2]/td[3]//text()')
        cha_one_month = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[3]/td[3]//text()')
        sum_one_month = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[4]/td[3]//text()')
        # 最近6个月
        hao_six_month = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[1]/td[4]//text()')
        zhong_six_month = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[2]/td[4]//text()')
        cha_six_month = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[3]/td[4]//text()')
        sum_six_month = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[4]/td[4]//text()')
        # 6个月前
        hao_six_month_ago = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[1]/td[5]//text()')
        zhong_six_month_ago = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[2]/td[5]//text()')
        cha_six_month_ago = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[3]/td[5]//text()')
        sum_six_month_ago = html.xpath('//*[@id="new-rate-content"]/div[1]/div[2]/table[2]/tbody/tr[4]/td[5]//text()')

        buyerGrandCredit = int(xinyong[0])
        praiseRate = comment[0]
        response = {
            '买家累积信用': buyerGrandCredit,
            '好评率': praiseRate,
            '好评': {
                '最近1周': int(hao_one_week[0]),
                '最近1个月': int(hao_one_month[0]),
                '最近6个月': int(hao_six_month[0]),
                '6个月前': int(hao_six_month_ago[0]),
                '总计': int(hao_num[0])
            },
            '中评': {
                '最近1周': int(zhong_one_week[0]),
                '最近1个月': int(zhong_one_month[0]),
                '最近6个月': int(zhong_six_month[0]),
                '6个月前': int(zhong_six_month_ago[0]),
                '总计': int(zhong_num[0])
            },
            '差评': {
                '最近1周': int(cha_one_week[0]),
                '最近1个月': int(cha_one_month[0]),
                '最近6个月': int(cha_six_month[0]),
                '6个月前': int(cha_six_month_ago[0]),
                '总计': int(cha_num[0])
            },
            '总计': {
                '最近1周': int(sum_one_week[0]),
                '最近1个月': int(sum_one_month[0]),
                '最近6个月': int(sum_six_month[0]),
                '6个月前': int(sum_six_month_ago[0]),
                '总计': int(sum[0])
            }

        }
        print(response)
        print('获取评价成功')
        return response
    except IndexError as e:
        print('获取好中差评数 数组下标越界', e)


# 猜你喜欢
def guess_you_like(cookie):
    list = []
    guess_you_like_url = 'https://i.taobao.com/my_taobao_api/guess_you_like.json'
    response = requests.get(url=guess_you_like_url, cookies=cookie)
    data = response.json().get('data')
    for item in data:
        itemName = item.get('itemName')
        itemPic = item.get('itemPic')
        itemUrl = item.get('itemUrl')
        itemPrice = item.get('itemPrice')
        itemInfo = {
            '宝贝名': itemName,
            '图片': itemPic,
            '地址': itemUrl,
            '价格': itemPrice,
        }
        list.append(itemInfo)
    print(list)
    return list


# 获取订单
def get_order(cookie):
    # form_data = 'pageNum=2&pageSize=15&prePageNo=1'
    pageNum = 2
    pageSize = 20
    prePageNo = 1
    waitRateNum = 0
    orderData = []
    print('开始获取所有订单')
    order_url = 'https://buyertrade.taobao.com/trade/itemlist/asyncBought.htm'
    form_data = {
        'pageNum': pageNum,
        'pageSize': pageSize,
        'prePageNo': prePageNo,
    }

    try:
        response = requests.post(url=order_url, headers=ORDER_HEADER, cookies=cookie, data=form_data)
        if response.status_code == 200:
            if response:
                data = response.json()
                if data:
                    if data.get('error') == "":
                        pageNum = int(data.get('page').get('currentPage')) + 1
                        totalNumber = data.get('page').get('totalNumber')
                        tabs = data.get('tabs')
                        if tabs[1].get('count'):
                            waitPayNum = tabs[1].get('count')
                        if tabs[2].get('count'):
                            waitSendNum = tabs[2].get('count')
                        if tabs[3].get('count'):
                            waitConfirmNum = tabs[3].get('count')
                        waitRateNum = tabs[4].get('count') if tabs[4].get('count') else waitRateNum

                        orders = data.get('mainOrders')
                        for order in orders:
                            # 进一步解析订单内容
                            shopName = order.get('seller').get('shopName')
                            shopUrl = order.get('seller').get('shopUrl')
                            payInfo = order.get('payInfo').get('actualFee')
                            statusInfo = order.get('statusInfo').get('text')
                            Item = {}
                            for item in order.get('subOrders'):
                                itemTitle = item.get('itemInfo').get('title')
                                itemUrl = item.get('itemInfo').get('itemUrl')
                                itemPic = item.get('itemInfo').get('pic')
                                price = item.get('priceInfo').get('realTotal')
                                Item = {
                                    'itemTitle': itemTitle,
                                    'itemUrl': itemUrl,
                                    'itemPic': itemPic,
                                    'price': price,
                                }
                            Order = {
                                'shopName': shopName,
                                'shopUrl': shopUrl,
                                'payInfo': payInfo,
                                'statusInfo': statusInfo,
                                'item': Item,
                            }
                            orderData.append(Order)
                    else:
                        print('解析订单Error')
                        raise Exception
                else:
                    print('订单记录空')
        try:
            pageNum = int(data.get('page').get('totalPage'))
            prePageNo = pageNum - 1
            form_data = {
                'pageNum': pageNum,
                'pageSize': pageSize,
                'prePageNo': prePageNo,
            }
            response = requests.post(url=order_url, headers=ORDER_HEADER, cookies=cookie,
                                     data=form_data)
            if response.status_code == 200:
                if response:
                    data = response.json()
                    if data.get('error') == "":
                        order = data.get('mainOrders')
                        item = order[len(order) - 1]
                        createDay = item.get('orderInfo').get('createDay')
                        print(createDay)
                        TaoAge = calculating_time(createDay)
                        print(TaoAge)
                        print('获取淘龄结束')
        except Exception as e:
            print('获取淘龄信息Error', e)
    except Exception as e:
        print('获取所有订单Error', e)
    print(totalNumber)
    response = {
        '订单数': totalNumber,
        '订单': orderData,
    }
    return response


# 获取收藏信息
def get_collect(cookie):
    shopSum = 0
    shopInfo = []
    commoditySum = 0
    commodityInfo = []
    for row in range(0, 100):
        row = row * 6
        now = int(time.time() * 1000)
        collect_shop_url = 'https://shoucang.taobao.com/nodejs/shop_collect_list_chunk.htm?ifAllTag=0&tab=0&categoryCount=0&tagName=&type=0&categoryName=&needNav=false&startRow={row}&t={time}'.format(
            row=row, time=now)
        response = requests.get(url=collect_shop_url, cookies=cookie)
        try:
            if re.search('\S', response.content.decode()):
                html = etree.HTML(response.content.decode())
                collect_shopname = html.xpath('//a[@class="shop-name-link"]/@title')
                collect_shopurl = html.xpath('//a[@class="shop-name-link"]/@href')
                collect_shoppic = html.xpath('//div[@class="logo J_ShopClassTri"]/a/img/@src')
                for i in range(0, len(collect_shopname)):
                    collect_shop = {
                        '店铺名': collect_shopname[i],
                        '店铺地址': collect_shopurl[i],
                        '店铺logo': collect_shoppic[i],
                    }
                    shopInfo.append(collect_shop)

                # print(collect_shopname)
                shopSum += len(collect_shopname)
            else:
                print('shop_sum', shopSum)
                break
        except UnicodeDecodeError as e:
            print('获取用户收藏店铺 编码格式错误', e)
            return
    for row in range(0, 100):
        row = row * 30
        now = int(time.time() * 1000)
        collect_commodity_url = 'https://shoucang.taobao.com/nodejs/item_collect_chunk.htm?ifAllTag=0&tab=0&tagId=&categoryCount=0&type=0&tagName=&categoryName=&needNav=false&startRow={row}&t={time}'.format(
            row=row, time=now)
        response = requests.get(url=collect_commodity_url, cookies=cookie)
        try:
            if re.search('\S', response.content.decode()):
                html = etree.HTML(response.content.decode())
                collect_commodity_name = html.xpath('//li/div[2]/a/text()')
                collect_commodity_pic = html.xpath('//img[@class="img-controller-img"]/@src')
                collect_commodity_url = html.xpath('//a[@class="img-controller-img-link"]/@href')
                # collect_commodity_price = html.xpath('//div[@class="g_price"]/strong/text()')
                try:
                    for i in range(0, len(collect_commodity_name)):
                        collect_commodity = {
                            '宝贝名': collect_commodity_name[i],
                            '宝贝图片': collect_commodity_pic[i],
                            '宝贝地址': collect_commodity_url[i],
                            # '宝贝价格': collect_commodity_price[i],
                        }
                        commodityInfo.append(collect_commodity)
                    print(collect_commodity_name)
                except IndexError as e:
                    print('下标越界', e)
                commoditySum += len(collect_commodity_name)
            else:
                print('commodity_sum', commoditySum)
                break
        except UnicodeDecodeError as e:
            print('获取用户收藏宝贝 编码格式错误', e)
            return
    return {
        '收藏的宝贝': commoditySum,
        '收藏的店铺': shopSum,
    }


# 获取用户信息
def get_info(cookie):
    resp = requests.get(url=USERINFO_URL, cookies=cookie)
    # resp = requests.get(url=USERINFO_URL)
    html = etree.HTML(resp.content)
    try:
        user = html.xpath('//*[@id="main-content"]/dl/dd[1]/ul/li[1]/span[2]/text()')
        if len(user) > 0:
            user = user[0]
            print(user)
        else:
            user = None
        email = html.xpath('//*[@id="main-content"]/dl/dd[1]/ul/li[2]/span[2]/text()')
        if len(email) > 0:
            email = email[0]
            print(email)
        else:
            email = None
        phone = html.xpath('//*[@id="main-content"]/dl/dd[1]/ul/li[4]/span[2]/text()')
        if len(phone) > 0:
            phone = phone[0].strip()
            print(phone)
        else:
            phone = None
        # 用户认证
        authenticate = html.xpath('//*[@id="main-content"]/dl/dd[3]/ul/li[1]/div[1]/span/text()')
        if authenticate:
            authenticate = authenticate[0]
        else:
            authenticate = u'已认证'
        if authenticate == u"已完成":
            authenticate = u'已认证'
            print(authenticate)
        # user = html.xpath('//*[@id="main-content"]/dl/dd[1]/ul/li[1]/span[2]/text()')
        # print(user)
        resp = requests.get(url=BASEINFO_URL, cookies=cookie)
        html = etree.HTML(resp.content)
        name = html.xpath('//*[@id="J_uniqueName-mask"]/@value')
        if len(name) >= 1:
            username = name[0]
            print(username)
        pattern = re.compile(r'selected="selected".*?>(.*?)</option>')
        result = re.findall(pattern, resp.text)
        if result:
            print(result[0])
            try:
                year = int(result[0])
                age = 2018 - year
            except ValueError as e:
                print('类型转换错误', e)
                year = 0
                age = 0
        print('获取用户信息成功')
    except IndexError as e:
        print('获取用户信息数组下标越界', e)
    response = {
        '用户ID': user,
        '用户名': username,
        '用户邮箱': email,
        '手机号': phone,
        '出生年': year,
        '年龄': age,
        '认证': authenticate,
    }
    return response


def get_user(cookie):
    resp = requests.get(url=USERINFO_URL, cookies=cookie)
    # resp = requests.get(url=USERINFO_URL)
    html = etree.HTML(resp.content)
    user = html.xpath('//*[@id="main-content"]/dl/dd[1]/ul/li[1]/span[2]/text()')
    if len(user) > 0:
        user = user[0]
        print(user)
    return user


def get_foot(cookie):
    pass


if __name__ == '__main__':
    pass
