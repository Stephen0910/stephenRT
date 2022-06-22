#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/6/21 9:50
# @Author   : StephenZ
# @Site     : 
# @File     : p_diff.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import requests, json
import http.client

u1 = "https://api.lolicon.app/setu/v2"
u2 = "http://moe.jitsu.top/img/?sort=r18&size=original&type=json&num=2"  # 略差

headers = {
    'authority': 'api.lolicon.app',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}


async def st1():
    data = {
        "r18": 1,
        "num": 2,
        "proxy": "i.pixiv.re"
    }
    with requests.post(url=u1, json=data, headers=headers, timeout=5) as session:
        response = json.loads(session.text)
        urls = []
        if response["error"] == "":
            for i in response["data"]:
                urls.append(i["urls"]["original"].replace("i.pixiv.cat", "i.pixiv.re"))
                # urls.append(i["urls"]["original"])
            return urls[0]
        else:
            return response["error"]


async def st2():
    with requests.get(u2) as session:
        response = json.loads(session.text)
        if response:
            return response["pic"][0]
