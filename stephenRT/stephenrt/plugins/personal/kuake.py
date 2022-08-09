#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/8/3 16:35
# @Author   : StephenZ
# @Site     : 
# @File     : kuake.py
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


k_url = "https://act.quark.cn/apps/qknewshours/routes/hot_news"
detail = "https://iflow-news.quark.cn/r/quark-iflow/landing/?item_id="
base_url = "https://iflow.uc.cn/webview/news?app=&aid="
base = "https://iflow.uczzd.cn/iflow/api/v1/article/aggregation?__t=1659609915000&aggregation_id=16665090098771297825&count=10"

k_headers = {
    'authority': 'act.quark.cn',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
    'cache-control': 'max-age=0',
    'cookie': '__itrace_wid=45600877-d7a2-4c97-3019-c6ea09f0807e; omelette-vid=595067458491968026987426; omelette-vid.sig=SV4W2Av3Ww6f0v08FvdNcHrKC2VBCezHTf4Te5J2ED8; b-user-id=f919e062-dd90-ff8c-f7a8-0b6726ad18e9',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36'
}


u_headers = {
    'authority': 'iflow.uc.cn',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
    'cache-control': 'max-age=0',
    'cookie': '__wpkreporterwid_=93d89238-09f4-4e51-bd55-77dbfee29f9b; cna=Qu0tGxxCmlgCAavdkbRFoQG9; ctoken=Ldk13z9-eEpjBsZiYAdyXiqc; sn=adfca447-bc88-4a55-aad2-ca314a28af79; isg=BHh4lZtWbiuax4K0F8Prw9ZhSSYK4dxr1fjDZrLpybNmzRi3WvRy-xHvgcX9m5RD',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}


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


def timestamp(string):
    """
    没有根据日期来判断 取的是前一天
    :param string:
    :return:
    """
    string = str(string)
    date = int(time.mktime(datetime.date.today().timetuple()))
    if re.match("\d\d/\d\d ", string):
        date -= 86400
        mininte = [int(x) for x in string.split(" ")[1].split(":")]

    else:
        mininte = [int(x) for x in string.split(":")]
    timestamp = mininte[0] * 3600 + mininte[1] * 60 + date
    return timestamp


# async def news_list():
#     with requests.get(url=k_url, headers=k_headers) as session:
#         full = []
#         soup = BeautifulSoup(session.content, "html.parser")
#         times = soup.find_all(name='div', attrs={"class": "rax-view-v2 date"})
#         # month = soup.find(name="div", attrs={"class": "rax-view-v2 schedule-month"})
#         # day = soup.find_all(name="div", attrs={"class": "rax-view-v2 schedule-day"})
#         # print(day[-1].text)
#
#         for p in times:
#             p_time = p.string
#             full.append(p_time)
#
#         titles = soup.find_all(name="div", attrs={"class": "rax-view-v2 article-item-title"})
#         for i in titles:
#             full.append(i.string)
#
#         # content 有bug
#         # contents = soup.find_all(name="div", attrs={"class": "rax-view-v2 article-item-text", "style": ""})
#         # for index, i in enumerate(contents):
#         #     if i.string != None:
#         #         full.append(i.string)
#
#         #  img 暂停
#
#         sources = soup.find_all(name="div", attrs={"class": "rax-view-v2 article-item-source"})
#         for source in sources:
#             full.append(source.text[3:])
#
#         ids = soup.find_all(attrs={"class": "rax-view-v2 article-item-container", "style": ""})
#         for id in ids:
#             full.append(id["observeid"])
#
#         return full


# async def get_news():
#     with requests.get(url=k_url, headers=k_headers) as session:
#         soup = BeautifulSoup(session.content, "html.parser")
#         all_contents = soup.find_all("div", attrs={"class": "rax-view-v2 aiticle-list-box"})  # 所有内容
#         times_soup = all_contents[0].find_all(name="div", attrs={"class": "rax-view-v2 date"})
#         some = all_contents[0].find_all(name="div", attrs={"data-c": "news"})
#         news = [x["data-exposure-extra"] for x in some]
#         every = all_contents[0].find_all(name="div", attrs={"class": "rax-view-v2 article-item-content"})
#         # imgs = [img.find_all("img")[0]["src"] if re.search("http", img.find_all("img")[0]["src"]) else None for img in
#                 # every]
#         every = all_contents[0].find_all(name="div", attrs={"class": "rax-view-v2 article-item-inner-text graphics-mode"})
#         imgs = []
#         for item in every:
#             try:
#                 img = item.find_all("img")[0]["src"]
#             except:
#                 img = ""
#             finally:
#                 imgs.append(img)
#         times = [time.text for time in times_soup]
#         urls = [parse.unquote(json.loads(url)["url"]) for url in news]
#         source_names = [(json.loads(source_name)["source_name"]) for source_name in news]
#         titles = [(json.loads(title)["title"]) for title in news]
#         ids = [json.loads(id["data-exposure-extra"])["id"] for id in some]
#         return [times, titles, source_names, urls, imgs, ids]


async def news10():
    with requests.get(base, headers=u_headers) as session:
        return json.loads(session.content)


news = on_metaevent()

first_time = int(time.time())
trigger = 1

ip = get_host_ip()
if ip == "10.10.10.8":
    # first_time = 1659593905

    first_time = int(round(time.time() * 1000))
    # group = 959822848  移除
    group = 755489024
    mis_category = ["国际足球", "股票", "财经", "期货", "旅游"]
elif ip == "172.24.121.72":
    first_time = int(round(time.time() * 1000))
    group = 157875133
    mis_category = []

else:
    # first_time = 1659938650000
    first_time = int(round(time.time() * 1000))
    group = 755489024
    mis_category = []


@news.handle()
async def news_report():
    global trigger, first_time
    msg = ""
    print(time.strftime("%m-%d, %H:%M:%S", time.localtime(int(time.time()))), "kuake trigger: {0}".format(trigger))
    if trigger % 6 == 0:
        print("push report")
        bot = get_bot()
        # news = await news_list()
        response = await news10()

        # for i in range(9):
        #     if timestamp(news[0][i]) > first_time:
        #         pic = MessageSegment.image(news[4][i]) if news[4][i] != "" else ""
        #         # url = ps.Shortener().clckru.short(news[3][i]) # 无法识别
        #         url = base_url + news[5][i]
        #         msg = msg + "【{1} {0}】{2}\n {3}".format(news[0][i], news[2][i], news[1][i], url) + pic + "\n"
        #     else:
        #         break
        # if timestamp(news[0][0]) > first_time:
        #     first_time = timestamp(news[0][0])

        if response["status"] != 0:
            print(response["message"])
            await bot.send_private_msg(user_id=281016636, message=response["message"])

        articles = response["data"]["articles"]
        for article in articles:
            # 条件
            if len(set(mis_category) & set(article["category"])) == 0 and article["doc_ext_obj"][
                "is_breaking_news"] is True:
                m_time = article["publish_time"]
                url = base_url + str(article["id"])
                source = article["source_name"]
                title = article["title"]
                summary = article["summary"]
                try:
                    pic_url = article["thumbnails"][0]["url"]
                except:
                    pic_url = ""
                if m_time > first_time:
                    nature = datetime.datetime.fromtimestamp(m_time / 1000).strftime("%H:%M")
                    if pic_url != "":
                        pic = MessageSegment.image(pic_url)
                    else:
                        pic = ""
                    msg = msg + "【{0} {1}】 {2}\n        {3}{4}".format(source, nature, title, summary, url) + pic + "\n"
                else:
                    break
            else:
                print("dislike:", article["title"])

        first_time = articles[0]["publish_time"] if articles[0]["publish_time"] > first_time else first_time

        print("msg::", msg)

    if msg != "":
        # await bot.send_private_msg(user_id=281016636, message=msg)
        try:
            await bot.send_group_msg(group_id=group, message=msg)
        except Exception as e:
            await bot.send_private_msg(user_id=281016636, message=msg + str(e))
    trigger += 1
