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
import os, subprocess

import requests

url = "https://play.google.com/store/apps/details?id=endless.nightmare.shrine.horror.scary.free.android"
proxies = {"http": "127.0.0.1:7890", "https": "127.0.0.1:7890"}
payload = {}
headers = {
    'authority': 'play.google.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'NID=511=jxCIt07QkMJW87SQi9Ide6SWYJAF0qRCJUHvfjQ0T6ZkHD6pNgPmokdHWrLCx_vDrrMfDSMWNtEQJTouC5jL7jh7hgPHYonwiObmcTzHCghlfS1RyyLxKilpl2de2iTe8fnG8h6lx4Zurv6xC7IwVH1_dyCtQTrh53YTSG1b8LU; _ga=GA1.3.1554811943.1660211631; _gid=GA1.3.1743682761.1660211631; OTZ=6631794_24_24__24_',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-arch': '"x86"',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-full-version': '"103.0.5060.134"',
    'sec-ch-ua-full-version-list': '".Not/A)Brand";v="99.0.0.0", "Google Chrome";v="103.0.5060.134", "Chromium";v="103.0.5060.134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"10.0.0"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

response = requests.request("GET", url, headers=headers, data=payload, proxies=proxies)

# print(response.text)


# import aiohttp
# import asyncio
#
#
# async def main():
#     con = aiohttp.TCPConnector(ssl=False)
#     async with aiohttp.ClientSession(connector=con, trust_env=True) as session:
#         async with session.get(url, proxy="http://127.0.0.1:7890") as resp:
#             response = await resp.text(encoding="utf-8")
#             print(response)
#
# print(url)
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# loop.close()

# a = """You can request that data be deleted"]]],null,null,null,[[["2.71.3188"]],[[[31,"12"]],[[[19,"4.4"]]]],[["May 19, 2022"]]],null,null,null,["May 19, 2022",[null,"* Game performance optimized, give you a better gaming experience! Have fun in gau003"""

# print(re.search("\[\[\[\"\d+.\d+.*?]],", a))

