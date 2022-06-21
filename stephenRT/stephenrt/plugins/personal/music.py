#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/6/17 15:26
# @Author   : StephenZ
# @Site     : 
# @File     : music.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import requests, json


def search_all(key):
    url = "https://c.y.qq.com/splcloud/fcgi-bin/smartbox_new.fcg?jsonpCallback=cb&key={0}&callback=cb&_=1655450897079".format(key)
    print(url)
    payload = {}
    headers = {
        'authority': 'c.y.qq.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
    with requests.get(url=url, headers=headers, data=payload) as session:
        response = session.text.replace("cb(", "").replace("\n)", "")
        datas = json.loads(response)

    return datas


def search_song():
    url = "http://59.110.45.28/m/api/search"

    payload = "data=f71eKtUaT8EduAQB28MzEKINWuygiRYN3JtmL60_-B4xtX-IROx1OhA3SF1FcRzfENGmWi0Jz7A_&v=2"
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://tools.liumingye.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'Cookie': 'myfreemp3_lang=zh-cn'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


search_song()