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


def get_response(url):
    response = requests.get(url)
    response.close()
    return response.content


def new_id(old_id):
    url = "https://www.douyu.com/{0}".format(old_id)
    with requests.get(url) as session:
        page_html = etree.HTML(session.content)
        redict_url = page_html.xpath("/html/body/section/main/div[4]/div[1]/div[1]/div[1]/div[1]/div/a/@href")
        room_id = re.search("\d+\d", str(redict_url)).group()
    return room_id


a = get_mc()
print(a)
