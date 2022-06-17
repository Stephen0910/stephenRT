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

import requests

url = "https://china.nba.cn/stats2/season/schedule.json?countryCode=CN&days=7&locale=zh_CN&tz=%2B8"

payload={}
headers = {
  'authority': 'china.nba.cn',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
  'cookie': 'i18next=zh_CN; locale=zh_CN; AMCVS_248F210755B762187F000101%40AdobeOrg=1; countryCode=CN; s_cc=true; privacyV2=true; s_sq=%5B%5BB%5D%5D; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22181662f9fd3e-01dbf86a314dbf9-26021b51-2073600-181662f9fd4ca%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgxNjYyZjlmZDNlLTAxZGJmODZhMzE0ZGJmOS0yNjAyMWI1MS0yMDczNjAwLTE4MTY2MmY5ZmQ0Y2EifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22181662f9fd3e-01dbf86a314dbf9-26021b51-2073600-181662f9fd4ca%22%7D; AMCV_248F210755B762187F000101%40AdobeOrg=-1712354808%7CMCIDTS%7C19161%7CMCMID%7C64061681013499296691299490953705543050%7CMCAAMLH-1656042813%7C11%7CMCAAMB-1656042813%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1655445213s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.3.0; tp=2629; s_ppv=cn%253Astats%253Aplayers%253Astephen_curry%253Astats%2C36%2C36%2C937; s_gpv=no%20value; nbachina=MTY1NTQ0NDc2M3xrYXo5MFBnakpuS3N3NEdhTUVNenczTU9WRERoUnhNSVdua1B4d3dZaDVKNkJvTlQzTXprUm9LSTQ2NXFnYUJlNUNRYUNaY2V6TEd0eFFjVVB5aElxRFNvRFFONVJSR1l88A287OCivnKcLqlxhL4pij-LAmD0IF3bIITY7jica78=',
  'if-none-match': '"2842-49b34a4123c3cff0131190f2a5d396d4dba099a9"',
  'referer': 'https://china.nba.cn/schedule/',
  'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

