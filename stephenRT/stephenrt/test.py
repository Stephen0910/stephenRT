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

import requests
from bs4 import BeautifulSoup

site = "https://webconf.douyucdn.cn"

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/60.0.3112.78 Safari/537.36'}

url = "http://openapi.douyu.com/api/thirdPart/token"

with requests.get(url=url, headers=headers) as session:
    response = json.loads(session.text)
    traceId = response["traceId"]
    print(traceId)

room = "http://openapi.douyu.com/api/thirdPart/getRoomInfo"
data = {
    "rid": "5264153",
    "cid_type": 3,
    "cid": 3,
    "rw": 300,
    "rh": 300
}