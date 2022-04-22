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
import requests, random, time
from lxml import etree
import re
import json

headers = {
    "Remote Address": "127.0.0.1:7890",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Referrer Policy": "strict-origin-when-cross-origin",
    "referer": "https://tophub.today/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
}

base_url = "https://tophub.today/"

url_json = {
    "c": "munions",
    "t": "follow",
    "cid": 10
}

s = requests.get(base_url, headers=headers)
content = str(s.content.decode())
# print(content)

html = etree.HTML(content)
new_xpath = '//*[@id="Sortable"]'
title = '//*[@id="node-1"]/div/div[1]/div[1]/a/div/span/text()'
news = html.xpath(title)



s.close()
print(news)