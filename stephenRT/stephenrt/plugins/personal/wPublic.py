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

query = {"成都发布": "MzA4MTg1NzYyNQ==", "成都本地宝": "MzA4NzA4MDY5OQ=="}


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


# async def search_public(names):
#     create_times = []
#     pics = []
#     titles = []
#     urls = []
#     search_names = []
#     for name in names:
#         try:
#             search_url = "https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&begin=0&count=3&query={1}&token={0}&lang=zh_CN&f=json&ajax=1".format(
#                 token,
#                 name)
#             # print("search_url:", search_url)
#             with requests.get(search_url, headers=headers) as session:
#                 response = json.loads(session.text)
#                 print("res:", response)
#                 fake_id = response["list"][0]["fakeid"]
#
#             artcles_url = "https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin=0&count=5&fakeid={1}&type=9&query=&token={0}&lang=zh_CN&f=json&ajax=1".format(
#                 token,
#                 fake_id)
#             # print("artcles_url:", artcles_url)
#             with requests.get(artcles_url, headers=headers) as session:
#                 response = json.loads(session.text)
#             print(response)
#             for app_msg in response["app_msg_list"]:
#                 create_time = app_msg["create_time"]
#                 if create_time not in create_times:
#                     titles.append(app_msg["title"])
#                     urls.append(app_msg["link"])
#                     pics.append(app_msg["cover"])
#                     create_times.append(create_time)
#                     search_names.append(name)
#         except Exception as e:
#             print("{0} 获取失败:{1}".format(name, e))
#             continue
#
#         # for index, title in enumerate(titles):
#         #     print(name, title, create_times[index], pics[index], urls[index])
#     return [create_times, titles, urls, pics, search_names]

public_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': cook,
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}


async def get_news():
    result = {}
    payload = {}
    for key, value in query.items():
        url = "https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={0}&scene=124&".format(value)

        with requests.get(url, headers=public_headers, data=payload) as session:
            response = session.text

        msg_contents = re.findall("msgList =.*?\';", response)[0]
        msg_str = msg_contents.replace("&quot;", "\'")[11:-2].replace("\'", "\"")
        msg_json = json.loads(msg_str)
        result[key] = msg_json
    return result


first_time = int(time.time())
trigger = 1

ip = get_host_ip()
first_time = int(time.time())

if ip == "10.10.10.8":
    # group = 959822848  移除
    group = 755489024
    mis_category = ["国际足球", "股票", "财经", "期货", "旅游"]
elif ip == "172.24.121.72":
    group = 755489024
    mis_category = []

else:
    first_time = 1660098904
    group = 755489024
    mis_category = []


public = on_metaevent()


@public.handle()
async def public_push():
    global trigger, first_time
    msg = ""
    print(time.strftime("%m-%d, %H:%M:%S", time.localtime(int(time.time()))), "public trigger: {0}".format(trigger))
    if trigger % 3 == 0:
        print("push public")
        bot = get_bot()
        # news = await news_list()
        news = await get_news()
        # print("tttttt:\n", time.strftime("%m-%d, %H:%M:%S", time.localtime(int(time.time()))), json.dumps(news))
        for key, value in news.items():
            news_list = value["list"]
            for each_new in news_list:
                comm_msg_info, app_msg_ext_info = each_new.values()
                p_time = comm_msg_info["datetime"]
                title = app_msg_ext_info["title"]
                content_url = str(app_msg_ext_info["content_url"])
                url = str(content_url).replace("amp;", "").replace("amp;", "").split("&chksm=")[0]
                cover = app_msg_ext_info["cover"]
                if p_time > first_time:
                    pic = MessageSegment.image(cover)
                    nature = time.strftime("%H:%M", time.localtime(p_time))
                    msg = msg + "【公众号-{0} {1}】 {2}\n{3}\n".format(key, nature, title, url) + pic + "\n"
                else:
                    break

            if value["list"][0]["comm_msg_info"]["datetime"] > first_time:
                first_time = news_list[0]["comm_msg_info"]["datetime"]

        if msg != "":
            print(msg)
            try:
                await bot.send_group_msg(group_id=group, message=msg)
            except Exception as e:
                await bot.send_private_msg(user_id=281016636, message=msg + str(e))

    trigger += 1
