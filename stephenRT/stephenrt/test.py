#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/2/16 8:28
# @Author   : StephenZ
# @Site     : 
# @File     : test.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>
# !/usr/bin/env python3
# coding: utf-8

import re
from lxml import etree
import requests
import time
import json
import urllib

# a = "user_id=5272&openudid=1932009e83f13eb6&appname=candycruise&client_time=1654566440&appversion=19.7.3051&platform=GP&packagename=com.gameone.candycruiseswap.free&dataversion=337&adjust_adid=63201937c1214dde6aba2f5055160a0a&adjust_gpsadid=e24b8970-a227-433e-a147-cd40c24327ae&adjust_idfa=&onesignal_playerid=&fbase_forecast_pay=0&fbase_forecast_away=0&timezone_offset=28800&dynamic_code=753347&country=CN&systemversion=8.0.0&devicemodle=SM-G9350&request_type=getIAPItemData"
#
# import json
#
# raw_dict = {}
# for item in a.split("&"):
#     data = item.split("=")
#     raw_dict[str(data[0])] = data[1]
# print(json.dumps(raw_dict))
#
# for key,value in raw_dict.items():
#     print(key, ":", value)
#

# import requests
#
# with requests.get("https://imyshare.com/hot-girl/") as session:
#   print(session.text)
#   page_html = etree.HTML(session.text)
#   src = page_html.xpath("/html/body/div[2]//@src")[0]
#   print(src)

def transfer_time(timestamp):
    timestamp = int(timestamp)
    if timestamp > 3653284221:
        query_time = round(timestamp / 1000)
        nature = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(query_time))
    else:
        nature = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
    return nature


url = "https://china.nba.cn/stats2/season/schedule.json?countryCode=CN&days=7&locale=zh_CN&tz=+8"
with requests.get(url) as session:
    response = json.loads(session.text)
    dates = response["payload"]["dates"]
    for date in dates:
        games = date["games"]
        for game in games:
            profile = game["profile"]  # 基本信息
            boxscore = game["boxscore"]  # 比分信息
            urls = game["urls"]  # 腾讯直播地址
            broadcasters = game["broadcasters"]  # 其他直播地址
            homeTeam = game["homeTeam"]  # 主场信息
            awayTeam = game["awayTeam"]  # 客场信息
            nature = transfer_time(profile["utcMillis"])

            print("⬤  {0} 主场:{1} 客场:{2} \n".format(nature, homeTeam["profile"]["displayAbbr"], awayTeam["profile"]["displayAbbr"]))
