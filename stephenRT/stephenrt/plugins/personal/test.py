#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/8/4 10:44
# @Author   : StephenZ
# @Site     : 
# @File     : test.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import requests, json
from bs4 import BeautifulSoup
from urllib import parse
import base64
import re, random

k_url = "https://act.quark.cn/apps/qknewshours/routes/hot_news"
base_url = "https://iflow.uc.cn/webview/news?app=&aid="
k_headers = {
    'authority': 'act.quark.cn',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
    'cache-control': 'max-age=0',
    'cookie': '__itrace_wid=45600877-d7a2-4c97-3019-c6ea09f0807e; omelette-vid=595067458491968026987426; omelette-vid.sig=SV4W2Av3Ww6f0v08FvdNcHrKC2VBCezHTf4Te5J2ED8; b-user-id=f919e062-dd90-ff8c-f7a8-0b6726ad18e9',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Mobile Safari/537.36'
}
link = "https://iflow-news.quark.cn/r/quark-iflow?&item_id="


def news_list():
    with requests.get(url=k_url, headers=k_headers) as session:
        soup = BeautifulSoup(session.content, "html.parser")
        all_contents = soup.find_all("div", attrs={"class": "rax-view-v2 aiticle-list-box"})  # 所有内容
        times_soup = all_contents[0].find_all(name="div", attrs={"class": "rax-view-v2 date"})
        some = all_contents[0].find_all(name="div", attrs={"data-c": "news"})
        news = [x["data-exposure-extra"] for x in some]
        every = all_contents[0].find_all(name="div", attrs={"class": "rax-view-v2 article-item-inner-text graphics-mode"})
        imgs = []
        for item in every:
            try:
                img = item.find_all("img")[0]["src"]
            except:
                img = ""
            finally:
                imgs.append(img)

        times = [time.text for time in times_soup]
        urls = [parse.unquote(json.loads(url)["url"]) for url in news]
        source_names = [(json.loads(source_name)["source_name"]) for source_name in news]
        titles = [(json.loads(title)["title"]) for title in news]
        # print(times)
        # print(urls)
        for url in urls:
            print(url)
        # print(source_names)
        # print(titles)
        # for index, i in enumerate(imgs):
        #     print(index, i)

        for i in some:
            print(i["data-exposure-extra"])

        for i in some:
            print(json.loads(i["data-exposure-extra"])["id"])

        ids = [json.loads(id["data-exposure-extra"])["id"] for id in some]
        print(ids)

        urls = [base_url+id  for id in ids]
        for url in urls:
            print(url)


a = """
https://mp.weixin.qq.com/s?__biz=MzA4MTg1NzYyNQ==&mid=2652452745&idx=1&sn=bc236e0fa6fbe1af9d7f4912644d1c2b&chksm=84630abfb31483a98dfc4260589c97d68cf6036061a0d1191e2a83ea9f6808787f562e9dd515#rd
"""
print(a.split("&chksm")[0])

