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

headers = {
    "Cookie": "connect.sid=s%3AP5UKa3BieRaSXePQMui8YXyIHf4-Rdl_.aeUiZBvjuSERszP%2FKIji8R0DmYZYRY8q53JdcbHcTYc; search_type=room; _ga=GA1.2.511076242.1652323852; history_search_fan=[{}]; _gid=GA1.2.2101712291.1654477272; _gat=1"
}

with requests.get(url="https://www.doseeing.com/data/api/rank?rids=5264153&dt=0&rank_type=chat_pv",
                  headers=headers) as session:
    print(session.text)
