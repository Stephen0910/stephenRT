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


for i in range(1,100000):
    url = "https://webconf.douyucdn.cn/resource/common/gift/gift_template/{0}.json".format(i)
    with requests.get(url=url) as session:
        if session.status_code == 200:
            print(i)
            data = session.text.replace('DYConfigCallback(', '')[0:-2]
            if "野摩托" in data:
                print(data)