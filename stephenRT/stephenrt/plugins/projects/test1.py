#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/4/22 17:39
# @Author   : StephenZ
# @Site     : 
# @File     : test1.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import requests, json
import websockets
import asyncio
import re

text_check = ["鉆|钻|砖|钴|万|萬|澫", "s|元|沅|钱|q|秋秋"]
name_check = ["3564837153|2580237802|166345259|3569544846|2927295662|1327004801|万钻|万钴|万砖|万鉆|萬鉆|萬钻|S级|S拍"]

a = "最强PK 5o=48澫钻时 Q  ③⑤③④①O⑧①④④ 货真价实，来了就是一家人"
b = "npcfauqjk"
c = "lccw411022"
print(re.search(text_check[0], a))

print(re.search(text_check[1], a.lower()))
print(re.match("[a-z]+|\d+", c))