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

a = {"name": 1}
print(a.items())


def dosee_info(id):
    d1 = "https://www.doseeing.com/data/api/topuser/{0}?type=gift&dt=0".format(id)
    d2 = "https://www.doseeing.com/data/api/topuser/{0}?type=chat&dt=0".format(id)
    with requests.get(d1, verify=False, timeout=3) as session:
        if session.status_code == 200:
            response = json.loads(session.text)["data"]

            pay = "今日付费排行：\n" + "".join(
                [str(x["rank"]) + ":" + x["user.nickname"] + " ￥{0}".format(x["gift.paid.price"] / 100) + "\n" for x in
                 response if x["rank"] < 4])
            print(pay)
    with requests.get(d2, verify=False, timeout=3) as session:
        if session.status_code == 200:
            response = json.loads(session.text)["data"]
            talk = "今日弹幕排行: \n" + "".join(
                [str(x["rank"]) + ":" + x["user.nickname"] + " {0} 条".format(x["chat.pv"]) + "\n" for x in response if
                 x["rank"] < 4])
            print(talk)

    return pay + talk

dosee_info(5645739)
