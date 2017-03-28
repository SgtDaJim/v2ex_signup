#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @File       : signup.py
# @Time       : 2017/3/24 10:30
# @Author     : Jim
# @GitHub     : https://github.com/SgtDaJim

import urllib.request
import urllib.parse
import http.cookiejar
from bs4 import BeautifulSoup
import re
from email_constructor import Email
import configparser

def build_opener():
    cookie = http.cookiejar.CookieJar()
    cookie_processor = urllib.request.HTTPCookieProcessor(cookie)
    opener = urllib.request.build_opener(cookie_processor)
    opener.addheaders = [("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:49.0) Gecko/20100101 Firefox/49.0"),
                         ("Referer", "http://cn.v2ex.com/signin"),
                         ("Origin", "http://cn.v2ex.com"),
                         ("Host", "cn.v2ex.com")]
    urllib.request.install_opener(opener)

def login():

    url = "http://cn.v2ex.com/signin"

    login_data = configparser.ConfigParser()
    login_data.read("user.ini")

    username = login_data.get("LoginInfo", "user")
    password = login_data.get("LoginInfo", "password")

    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "lxml")
    #print(soup)
    inputs = soup.find_all("input")
    #print(inputs)
    #print(inputs[1]["name"], inputs[2]["name"], inputs[3]["value"], inputs[5]["value"])

    # 构造登录参数
    params = {
        inputs[1]["name"]: username,
        inputs[2]["name"]: password,
        inputs[3]["name"]: inputs[3]["value"],
        inputs[5]["name"]: inputs[5]["value"]
    }

    # 参数urlencode
    params = urllib.parse.urlencode(params).encode("utf-8")

    # 模拟登录过程
    request = urllib.request.Request(url, params, method="POST")
    response = urllib.request.urlopen(request)
    # html = response.read().decode("utf-8")
    print(response.info())

def get_redeem():

    daily_mission_url = "http://cn.v2ex.com/mission/daily"
    request = urllib.request.Request(daily_mission_url, method="GET")
    request.add_header("Referer", "http://cn.v2ex.com/")
    response = urllib.request.urlopen(request)
    html = response.read().decode("utf-8")
    # print(html)

    soup = BeautifulSoup(html, "lxml")
    redeem_link_bottom = soup.find("input", type="button")
    redeem_link_js = redeem_link_bottom["onclick"]
    # print(redeem_link_js)
    redeem_link = re.search("location.href = '(.*)';", redeem_link_js).group(1)
    # print(redeem_link)

    redeem_link = "http://cn.v2ex.com" + redeem_link
    request = urllib.request.Request(redeem_link, method="GET")
    request.add_header("Referer", "http://cn.v2ex.com/mission/daily")
    response = urllib.request.urlopen(request)
    html = response.read().decode("utf-8")

    soup = BeautifulSoup(html, "lxml")
    # print(soup)
    email_msg = ""
    msg = soup.find("div", class_="message")
    if msg :
        msg = msg.get_text()
        # print(msg)
        div = soup.find_all("div", class_="cell")
        for d in div:
            dtext = d.get_text()
            if dtext.find("已连续登录") != -1:
                print(dtext)
                email_msg += dtext + "\n"

        balance_link_bottom = soup.find("input", type="button")
        balance_link_js = balance_link_bottom["onclick"]
        balance_link = re.search("location.href = '(.*)';", balance_link_js).group(1)
        # print(balance_link)

        balance_link = "http://cn.v2ex.com" + balance_link
        request = urllib.request.Request(balance_link, method="GET")
        request.add_header("Referer", "http://cn.v2ex.com/mission/daily")
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
        # print(html)
        soup = BeautifulSoup(html, "lxml")
        data_table = soup.find("table", class_="data")
        tr = data_table.find_all("tr")[1]
        tds = tr.find_all("td")
        print(tds[4].get_text() + "，余额：" + tds[3].get_text())
        email_msg += tds[4].get_text() + "，余额：" + tds[3].get_text() + "\n"

    else:
        print("领取失败或今天已经成功领取！")
        email_msg += "领取失败或今天已经成功领取！"

    return email_msg


if __name__ == "__main__":
    build_opener()
    login()
    email_msg = get_redeem()

    # 发送邮件
    email = Email(email_msg)
    email.send()

    print("运行结束。")
