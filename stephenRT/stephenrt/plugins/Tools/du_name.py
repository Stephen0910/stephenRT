#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/6/23 14:49
# @Author   : StephenZ
# @Site     : 
# @File     : du_name.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import requests, json

url = "https://ywtb.mps.gov.cn/newhome/api/cmcx/query"

headers = {
    'Accept': 'application/json',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'Cookie': 'SESSION=NjNhZjI4ZmUtMmY5Ni00NzZjLWEzNWEtNGEzNzYwYjhkZjJk; zh_choose=s',
    'Origin': 'https://ywtb.mps.gov.cn',
    'Referer': 'https://ywtb.mps.gov.cn/newhome/portal/cmcx',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}


def query_name(name):
    payload1 = {"xm": name, "xb": 1, "xzqh": "100000"}
    payload2 = {"xm": name, "xb": 2, "xzqh": "100000"}
    with requests.post(url=url, headers=headers, data=json.dumps(payload1)) as session:
        response = json.loads(session.text)
    if response["success"] == True:
        male = response["data"]["count"]
    else:
        return "查询失败: {}".format(response["reason"])

    with requests.post(url=url, headers=headers, data=json.dumps(payload2)) as session:
        response = json.loads(session.text)
    if response["success"] == True:
        famale = response["data"]["count"]
    else:
        return "查询失败: {}".format(response["reason"])

    return [male, famale]


print(query_name("张"))
