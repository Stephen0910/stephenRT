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


def get_mc():
    url = "https://www.doseeing.com/rank/chat/7day?category=9"
    content_num = 8
    mc_dict = {}
    with requests.get(url) as session:
        page_html = etree.HTML(session.content)
        text_list = page_html.xpath("/html/body/div/div[2]/main/div/div/div[2]/table[2]/tbody//text()")
        mc_num = int(len(text_list) / content_num)
        for i in range(mc_num):
            if text_list[i * content_num + 3] == "DOTA":
                room = page_html.xpath(
                    "/html/body/div/div[2]/main/div/div/div[2]/table[2]/tbody/tr[{0}]/td[2]/a/@href".format(i + 1))
                room_id = re.search("\d+", str(room)).group()
                mc_dict[text_list[i * content_num + 1]] = room_id
    return mc_dict

a = get_mc()
print(list(a.keys()), list(a.values()))
