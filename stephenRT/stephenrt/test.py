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
import subprocess

from infi.devicemanager import DeviceManager

dm = DeviceManager()
dm.root.rescan()
devices = dm.all_devices
for device in devices:
    for i in device.children:
        if "Android Composite ADB Interface" in str(i):
            print("Android:", device.children)
        if "Apple Mobile Device USB Composite Device" in str(i):
            print("iOS:", device.children)

