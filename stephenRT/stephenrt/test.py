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
import requests, random
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
import subprocess
import re

# with requests.get("http://tools.liumingye.cn/music/?page=audioPage&type=migu&name=将军") as session:
#     response = session.text
#     print(response)
#     page_html = etree.HTML(response)
#     path = "/html/body/div[2]/div[2]/div[3]/div[3]"
#     path1 = "/html/body/div[2]/div[2]/div[3]/div[3]/div/div"
#     data_element = page_html.xpath(path1)
#     print(data_element)


import openai

openai.api_key = ""




import openai
import time
# 设置API密钥

# 定义问题和上下文
question = "What is the meaning of life?"
context = "The meaning of life is a philosophical question concerning the significance of life or existence in general."
# 循环对话
while True:
    # 发送请求并获取响应
    response = openai.Completion.create(
        engine="davinci",
        prompt=context + "\nQ: " + question + "\nA:",
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None,
        timeout=60,
    )
    # 解析响应并打印回答
    answer = response.choices[0].text.strip()
    print("A: " + answer)
    # 提示下一个问题
    question = input("Q: ")
    # 等待一段时间，避免过于频繁地发送请求
    time.sleep(1)



