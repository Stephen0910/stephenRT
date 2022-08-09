#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/8/5 12:16
# @Author   : StephenZ
# @Site     : 
# @File     : wPublic.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>
import re, datetime
from bs4 import BeautifulSoup
import requests, socket
import json
import time, random
from urllib import parse
from nonebot import get_bot
from nonebot import on_metaevent
from nonebot.adapters.onebot.v11.message import MessageSegment
import stephenrt.privateCfg as cfg

config = cfg.config_content
cook = config["wcookie"]


# msgs_url = "https://mp.data258.com/article/category/"
# detail = "https://mp.data258.com"
#
query_names = ["成都本地宝", "成都发布", "蓉城政事"]
token = "1928018217"
#
# headers = {
#     'authority': 'mp.data258.com',
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'accept-language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
#     'cache-control': 'max-age=0',
#     'cookie': '_jpanonym="NTM4M2ExMmVkMTkxNjljZTMwODBjODcxYjQwOWZjYWMjMTY1OTY3MTUxMzcwMiMzMTUzNjAwMCNaRGMxT0daaE9HWXhNVEkzTkdObU5XSXdOR0l4TUdJd1lURXpPR05pTVRVPQ=="; Hm_lvt_fd96d661d046cdf677204a54cc6e59b6=1659671514; _jpuid="NDFjMmNiMWZjZDM4YThlZjY1ZjQwOTJmOTdkOTg3ZGIjMTY1OTY3MTk5NTY0NSMxNzI4MDAjT0RBNA=="; csrf_token=a222f5a7b4776b86e681753fb2b48476; Hm_lpvt_fd96d661d046cdf677204a54cc6e59b6=1659673511; csrf_token=a222f5a7b4776b86e681753fb2b48476',
#     'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': '"Windows"',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'none',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
# }
#
#
# def search_urls(names):
#     ids = []
#     for name in names:
#         url = "https://mp.data258.com/mp/search?type=category&key={0}&sort=".format(parse.quote(name))
#         with requests.get(url, headers=headers) as session:
#             soup = BeautifulSoup(session.content, "html.parser")
#         page = soup.find_all(name="a", attrs={"class": "mp-avatar"})
#         id = page[0]["href"].split("/")[-1]
#         ids.append(id)
#     urls = [msgs_url + url for url in ids]
#     return dict(zip(names, urls))
#
#
# def transfer_time(orin_time):
#     timeArray = time.strptime(orin_time, "%Y-%m-%d %H:%M")
#     # 转换为时间戳:
#     timestamp = int(time.mktime(timeArray))
#     return timestamp
#
#
# url_dict = search_urls(query_names)
#
#
# def get_msgs():
#     names = list(url_dict.keys())
#     urls = list(url_dict.values())
#     for index, url in enumerate(urls):
#         print(names[index])
#         with requests.get(url, headers=headers) as session:
#             soup = BeautifulSoup(session.content, "html.parser")
#             html = soup.select("body > div.layui-container > div > div > div > ul > li")
#             # print(html)
#             for i in html:
#                 new = i.text
#                 link_page = detail + i.find("a", attrs={"class": "jie-title"})["href"]
#                 title, time = [info for info in new.split("\n") if info != ""]
#                 print(time, transfer_time(time), title, link_page)

search_url = "https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&begin=0&count=5&query=成都发布&token=321344637&lang=zh_CN&f=json&ajax=1"
p_articles = "https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin=0&count=5&fakeid=MzA4MTg1NzYyNQ==&type=9&query=&token=321344637&lang=zh_CN&f=json&ajax=1"

headers = {
    'authority': 'mp.weixin.qq.com',
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
    'cookie': cook,
    'referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=10&token=321344637&lang=zh_CN',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.27.400 QQBrowser/9.0.2524.400',
    'x-requested-with': 'XMLHttpRequest'
}


def trasfer_timestamp():
    pass


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


async def search_public(names):
    create_times = []
    pics = []
    titles = []
    urls = []
    search_names = []
    for name in names:
        try:
            search_url = "https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&begin=0&count=3&query={1}&token={0}&lang=zh_CN&f=json&ajax=1".format(
                token,
                name)
            # print("search_url:", search_url)
            with requests.get(search_url, headers=headers) as session:
                response = json.loads(session.text)
                print("res:", response)
                fake_id = response["list"][0]["fakeid"]

            artcles_url = "https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin=0&count=5&fakeid={1}&type=9&query=&token={0}&lang=zh_CN&f=json&ajax=1".format(
                token,
                fake_id)
            # print("artcles_url:", artcles_url)
            with requests.get(artcles_url, headers=headers) as session:
                response = json.loads(session.text)
            print(response)
            for app_msg in response["app_msg_list"]:
                create_time = app_msg["create_time"]
                if create_time not in create_times:
                    titles.append(app_msg["title"])
                    urls.append(app_msg["link"])
                    pics.append(app_msg["cover"])
                    create_times.append(create_time)
                    search_names.append(name)
        except Exception as e:
            print("{0} 获取失败:{1}".format(name, e))
            continue

        # for index, title in enumerate(titles):
        #     print(name, title, create_times[index], pics[index], urls[index])
    return [create_times, titles, urls, pics, search_names]


first_time = int(time.time())
trigger = 1

ip = get_host_ip()
if ip == "10.10.10.8":
    first_time = int(time.time())
    group = 959822848
else:
    # first_time = 1659667001
    first_time = int(time.time())
    group = 755489024

public = on_metaevent()


@public.handle()
async def public_push():
    global trigger, first_time
    msg = ""
    print("public trigger: {0}".format(trigger))
    if trigger % 120 == 0:
        print("push public")
        bot = get_bot()
        # news = await news_list()
        news = await search_public(query_names)
        print("tttttt:\n", news)
        create_times, titles, urls, pics, names = news
        for index, create_time in enumerate(create_times):
            if create_time > first_time:
                pic = MessageSegment.image(pics[index])
                nature = time.strftime("%H:%M", time.localtime(create_time))
                url = urls[index].split("chksm")[0]
                msg = msg + "【{0} {1}】 {2}\n{3}\n".format(names[index], nature, titles[index], url) + pic + "\n"

        if max(create_times) > first_time:
            first_time = max(create_times)

        if msg != "":
            print(msg)
            try:
                await bot.send_group_msg(group_id=group, message=msg)
            except Exception as e:
                await bot.send_private_msg(user_id=281016636, message=msg + str(e))

    trigger += 1
