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

import requests, re, time, datetime
from bs4 import BeautifulSoup
import requests
import json
import time
from nonebot import on_command
from nonebot.rule import to_me
from nonebot import get_bot
from nonebot import on_metaevent

k_url = "https://act.quark.cn/apps/qknewshours/routes/hot_news"
detail = "https://iflow-news.quark.cn/r/quark-iflow/landing/?item_id="

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


async def news_list():
    with requests.get(url=k_url, headers=k_headers) as session:
        full = []
        soup = BeautifulSoup(session.content, "html.parser")
        times = soup.find_all(name='div', attrs={"class": "rax-view-v2 date"})
        # month = soup.find(name="div", attrs={"class": "rax-view-v2 schedule-month"})
        # day = soup.find_all(name="div", attrs={"class": "rax-view-v2 schedule-day"})
        # print(day[-1].text)

        for p in times:
            p_time = p.string
            full.append(p_time)

        titles = soup.find_all(name="div", attrs={"class": "rax-view-v2 article-item-title"})
        for i in titles:
            full.append(i.string)

        contents = soup.find_all(name="div", attrs={"class": "rax-view-v2 article-item-text", "style": ""})
        for index, i in enumerate(contents):
            if i.string != None:
                full.append(i.string)

        #  img 暂停

        ids = soup.find_all(attrs={"class": "rax-view-v2 article-item-container", "style": ""})
        for id in ids:
            full.append(id["observeid"])

        return full


news = on_metaevent()
# first_time = 1659582303
first_time = int(time.time())
trigger = 1
time_list = [first_time]


@news.handle()
async def news_report():
    global trigger, time_list
    msg = ""
    if trigger % 6 == 0:
        bot = get_bot()
        news = await news_list()
        print(news)

        for i in range(9):
            if timestamp(news[i]) > time_list[-1]:
                detail_url = detail + str(news[i + 30])
                msg += "{0}\n{1}\n{2}\n\n".format(news[i], news[i + 10], detail_url)
            else:
                break
        if timestamp(news[0]) > time_list[-1]:
            time_list.append(timestamp(news[0]))
        # time_list = list(set(time_list))
        print("msg")
        print(msg)
        print(time_list)
    if msg != "":
        # await bot.send_private_msg(user_id=281016636, message=msg)
        try:
            await bot.send_group_msg(group_id=959822848, message=msg)
        except Exception as e:
            await bot.send_private_msg(user_id=281016636, message=msg + str(e))
    trigger += 1
