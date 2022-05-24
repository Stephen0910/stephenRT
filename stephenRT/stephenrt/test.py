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

import requests
import time

url = "https://www.douyu.com/lapi/live/getH5Play/5264153"

data = {
    "v": 220120220524,
    "tt": int(time.time()),
    "did":"5f6f25a45d1b8be592e9330500071501",
    "sign": "5f6f25a45d1b8be592e9330500071501",
    "ver": "Douyu_222052005",
    "iar": 1
}

with requests.post(url=url, json=data) as session:
    print(session.content)