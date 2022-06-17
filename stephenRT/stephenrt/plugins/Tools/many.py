#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/6/16 17:17
# @Author   : StephenZ
# @Site     : 
# @File     : many.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

# 资源搜索
import requests, json

import http.client

conn = http.client.HTTPSConnection("doc.htmcdn.com", 39988)
payload = "word=%E7%91%9E%E5%85%8B&pageSize=5&pageNo=1"
headers = {
  'authority': 'doc.htmcdn.com:39988',
  'accept': '*/*',
  'accept-language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
  'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'origin': 'https://doc.htmcdn.com:39988',
  'referer': 'https://doc.htmcdn.com:39988/search-%E7%91%9E%E5%85%8B-rel-1.html?',
  'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
  'x-requested-with': 'XMLHttpRequest'
}
conn.request("POST", "/ad/list0", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))