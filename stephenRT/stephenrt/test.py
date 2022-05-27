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

orinTime = "2013-10-10 23:40:00"
# 将其转换为时间数组

try:
    input_time = re.findall("\d+", orinTime)
    shijian = "-".join(input_time)
    s_t = time.strptime(shijian, "%Y-%m-%d-%H-%M-%S")
    ts = str(int(time.mktime(s_t)))
    print(ts, type(ts))
except Exception as e:
    print(e)
    print("内部错误, 查询结束: {0}".format(str(e)))