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

def test():
    html = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html lang="zh-CN">
<head>
	<meta name="Content-Type" content="text/html;charset=utf-8" />
    <meta name="Referrer" content="unsafe-url" />
	<meta content="True" name="HandheldFriendly" />
	
    <meta name="detectify-verification" content="d0264f228155c7a1f72c3d91c17ce8fb" />
<meta name="alexaVerifyID" content="OFc8dmwZo7ttU4UCnDh1rKDtLlY" />
<meta name="baidu-site-verification" content="D00WizvYyr" />
<meta name="msvalidate.01" content="D9B08FEA08E3DA402BF07ABAB61D77DE" />
<meta property="wb:webmaster" content="f2f4cb229bda06a4" />
<meta name="google-site-verification" content="LM_cJR94XJIqcYJeOCscGVMWdaRUvmyz6cVOqkFplaU" />
    
    <title>V2EX › 日常任务</title>
    <link rel="dns-prefetch" href="//static.v2ex.com" />
    <link rel="dns-prefetch" href="//cdn.v2ex.com" />
    <link rel="dns-prefetch" href="//cdn.v2ex.co" />
    <link rel="dns-prefetch" href="//i.v2ex.co" />
    
        <link rel="stylesheet" type="text/css" media="screen" href="/css/basic.css?v=199834:1478239324:3.9.7.5" />
    
    <link rel="stylesheet" type="text/css" media="screen" href="/static/css/style.css?v=416609f46253c81f1226585249e3d16f" />
    <link rel="stylesheet" type="text/css" media="screen" href="/css/desktop.css?v=3.9.7.5" />
    <link rel="stylesheet" href="//v2ex.assets.uxengine.net/js/highlight/styles/tomorrow.css" type="text/css" />
    <script type="text/javascript" src="//v2ex.assets.uxengine.net/js/highlight/highlight.pack.js"></script>
    <link rel="icon" sizes="192x192" href="/static/img/v2ex_192.png" />
    <link rel="shortcut icon" href="/static/img/icon_rayps_64.png" type="image/png" />
    <link rel="stylesheet" type="text/css" href="/static/css/font-awesome.min.css?v=295235b28b6e649d99539a9d32b95d30" />
	<script src="/static/js/jquery.js?v=8fc25e27d42774aeae6edbc0a18b72aa" type="text/javascript"></script>
	<script src="/static/js/jquery-ui.js?v=ba23883b51f5f372d28755e199785526" type="text/javascript"></script>
	<script src="//v2ex.assets.uxengine.net/static/js/jquery.autosize.js?v=1.18.9" type="text/javascript"></script>
    <link href="/static/css/jquery.textcomplete.css?v=5a041d39010ded8724744170cea6ce8d" rel="stylesheet" />
    <script src="/static/js/lscache.min.js?v=bf403ab76d287d394375662defac76c3" type="text/javascript"></script>
    <script src="/static/js/v2ex.js?v=e7dc4d2997a27686c66f38d805f14499" type="text/javascript"></script>
    <link href="/static/js/select2/select2.css?v=2621fe97ae1aabca8661d60000147412" rel="stylesheet" />
    <script src="/static/js/select2/select2.min.js?v=3225a95b13ab51f570e2544751ee8320" type="text/javascript"></script>
    <link href="/static/js/selectboxit/selectboxit.css?v=5dc55d3860ef80ef1875d6800a5fbfa3" rel="stylesheet" >
    <script src="/static/js/selectboxit/selectboxit.min.js?v=379ece65af74a99ef6cd7ca21f8beb6e" type="text/javascript"></script>
    <meta name="description" content="" />
    
    
    
</head>
<body>
    <div id="Top">
        <div class="content">
            <div style="padding-top: 6px;">
            <table cellpadding="0" cellspacing="0" border="0" width="100%">
                <tr>
                    <td width="110" align="left"><a href="/" name="top" title="way to explore"><img src="//v2ex.assets.uxengine.net/site/logo@2x.png?m=1346064962" border="0" align="default" alt="V2EX" width="94" height="30" /></a></td>
                    <td width="auto" align="left">
                        <div id="Search"><form action="https://www.google.com" onsubmit="return dispatch()" target="_blank"><div style="width: 276px; height: 28px; background-size: 276px 28px; background-image: url('/static/img/qbar_light@2x.png'); background-repeat: no-repeat; display: inline-block;"><input type="text" maxlength="40" name="q" id="q" value="" /></div></form></div>
                    </td>
                    <td width="570" align="right" style="padding-top: 2px;"><a href="/" class="top">首页</a>&nbsp;&nbsp;&nbsp;<a href="/member/SgtDaJim" class="top">SgtDaJim</a>&nbsp;&nbsp;&nbsp;<a href="https://workspace.v2ex.com/" target="_blank" class="top">工作空间</a>&nbsp;&nbsp;&nbsp;<a href="/notes" class="top">记事本</a>&nbsp;&nbsp;&nbsp;<a href="/t" class="top">时间轴</a>&nbsp;&nbsp;&nbsp;<a href="/settings" class="top">设置</a>&nbsp;&nbsp;&nbsp;<a href="#;" onclick="if (confirm('确定要从 V2EX 登出？')) { location.href= '/signout?once=63194'; }" class="top">登出</a></td>
                </tr>
            </table>
            </div>
        </div>
    </div>
    <div id="Wrapper">
        <div class="content">
            
            <div id="Leftbar"></div>
            <div id="Rightbar">
                <div class="sep20"></div>
                
                    
                    <div class="box">
                        <div class="cell">
                            <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                <tr>
                                    <td width="48" valign="top"><a href="/member/SgtDaJim"><img src="//v2ex.assets.uxengine.net/avatar/5e5f/2dbd/199834_large.png?m=1478239324" class="avatar" border="0" align="default" style="max-width: 48px; max-height: 48px;" /></a></td>
                                    <td width="10" valign="top"></td>
                                    <td width="auto" align="left"><span class="bigger"><a href="/member/SgtDaJim">SgtDaJim</a></span>
                                        
                                    </td>
                                </tr>
                            </table>
                            <div class="sep10"></div>
                            <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                <tr>
                                    <td width="33%" align="center"><a href="/my/nodes" class="dark" style="display: block;"><span class="bigger">0</span><div class="sep3"></div><span class="fade">节点收藏</span></a></td>
                                    <td width="34%" style="border-left: 1px solid rgba(100, 100, 100, 0.4); border-right: 1px solid rgba(100, 100, 100, 0.4);" align="center"><a href="/my/topics" class="dark" style="display: block;"><span class="bigger">4</span><div class="sep3"></div><span class="fade">主题收藏</span></a></td>
                                    <td width="33%" align="center"><a href="/my/following" class="dark" style="display: block;"><span class="bigger">0</span><div class="sep3"></div><span class="fade">特别关注</span></a></td>
                                </tr>
                            </table>
                        </div>
                        <div class="cell">
                        <div style="width: 250px; background-color: #f0f0f0; height: 3px; display: inline-block; vertical-align: middle;"><div style="width: 43px; background-color: #ccc; height: 3px; display: inline-block;"></div></div>
                        </div>
                        
                        <div class="cell" style="padding: 5px;">
                            <table cellpadding="0" cellspacing="0" border="0" width="100%">
                                <tr>
                                    <td width="32"><a href="/new"><img src="/static/img/flat_compose.png?v=7d21f0767aeba06f1dec21485cf5d2f1" width="32" border="0" /></a></td>
                                    <td width="10"></td>
                                    <td width="auto" valign="middle" align="left"><a href="/new">创作新主题</a></td>
                                </tr>
                            </table>
                        </div>
                        <div class="inner"><div class="fr" id="money"><a href="/balance" class="balance_area" style="">72 <img src="//v2ex.assets.uxengine.net/static/img/silver.png" alt="S" align="absmiddle" border="0" style="padding-bottom: 2px;" /> 70 <img src="//v2ex.assets.uxengine.net/static/img/bronze.png" alt="B" align="absmiddle" border="0" /></a></div><a href="/notifications" class="fade">0 条未读提醒</a></div>
                        
                    </div>
                    
                    
                    
                    
                    <div class="sep20"></div>
                    

<div class="box">
    <div class="inner" align="center">
        <a href="https://shimo.im/doc/G3ckHEVF3f4qANHk" target="_blank"><img src="//v2ex.assets.uxengine.net/assets/sidebar/shimo_20170315_1.jpg" border="0" width="250" height="250" alt="石墨文档" /></a>
    </div>
    <div class="sidebar_compliance"><a href="/advertise" target="_blank">广告</a></div>
</div>


                    <div class="sep20"></div>
                    
                    
                    
                
            </div>
            <div id="Main">
                <div class="sep20"></div>
                
<div class="box">
    <div class="cell"><a href="/">V2EX</a> <span class="chevron">&nbsp;›&nbsp;</span> 日常任务</div>
    <div class="message" onclick="$(this).slideUp('fast');">已成功领取每日登录奖励</div>
    <div class="cell">
        
        <span class="gray"><li class="fa fa-ok-sign" style="color: #0c0;"></li> &nbsp;每日登录奖励已领取</span>
        <div class="sep10"></div>
        <input type="button" class="super normal button" value="查看我的账户余额" onclick="location.href = '/balance';" />
        
    </div>
    <div class="cell">已连续登录 131 天</div>
</div>

            </div>
            
            
        </div>
        <div class="c"></div>
        <div class="sep20"></div>
    </div>
    <div id="Bottom">
        <div class="content">
            <div class="inner">
                <div class="sep10"></div>
                    <div class="fr">
                        <a href="https://www.digitalocean.com/?refcode=1b51f1a7651d" target="_blank"><img src="//v2ex.assets.uxengine.net/assets/logos/do_blue.png" width="60" border="0" alt="DigitalOcean" /></a>
                    </div>
                    <strong><a href="/about" class="dark" target="_self">关于</a> &nbsp; <span class="snow">·</span> &nbsp; <a href="/faq" class="dark" target="_self">FAQ</a> &nbsp; <span class="snow">·</span> &nbsp; <a href="/p/7v9TEc53" class="dark" target="_self">API</a> &nbsp; <span class="snow">·</span> &nbsp; <a href="/mission" class="dark" target="_self">我们的愿景</a> &nbsp; <span class="snow">·</span> &nbsp; <a href="/advertise" class="dark" target="_self">广告投放</a> &nbsp; <span class="snow">·</span> &nbsp; <a href="/advertise/2016.html" class="dark" target="_self">鸣谢</a> &nbsp; <span class="snow">·</span> &nbsp; 1520 人在线</strong> &nbsp; <span class="fade">最高记录 2466</span> &nbsp; <span class="snow">·</span> &nbsp; <a href="/select/language"><img src="/static/img/lang_zhcn_32.png" align="absmiddle" border="0" width="20" alt="" /></a>
                    <div class="sep20"></div>
                    创意工作者们的社区
                    <div class="sep5"></div>
                    World is powered by solitude
                    <div class="sep20"></div>
                    <span class="small fade">VERSION: 3.9.7.5 · 25ms · UTC 12:23 · PVG 20:23 · LAX 05:23 · JFK 08:23<br />♥ Do have faith in what you're doing.</span>
                    <div class="sep20"></div>
                    <span class="f12 gray"><a href="http://www.miibeian.gov.cn/" target="_blank" rel="nofollow">沪ICP备16043287号-1</a></span>
                <div class="sep10"></div>
            </div>
        </div>
    </div>
    
    
    

    
    
    

    

    
	<script>
	  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
	  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
	  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
	  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

	  ga('create', 'UA-11940834-2', 'v2ex.com');
	  ga('send', 'pageview');

	</script>
    

    <script src="/static/js/jquery.textcomplete.min.js?v=43bfb325d9b6b784e680aa9eaef91925" type="text/javascript"></script>
    
</body>
</html>'''

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
                email_msg += dtext +"\n"

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
    #email_msg = test()

    # 发送邮件
    email = Email(email_msg)
    email.send()

    print("运行结束。")
