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
import requests, random
import time
import json
import urllib

# a = "user_id=5272&openudid=1932009e83f13eb6&appname=candycruise&client_time=1654566440&appversion=19.7.3051&platform=GP&packagename=com.gameone.candycruiseswap.free&dataversion=337&adjust_adid=63201937c1214dde6aba2f5055160a0a&adjust_gpsadid=e24b8970-a227-433e-a147-cd40c24327ae&adjust_idfa=&onesignal_playerid=&fbase_forecast_pay=0&fbase_forecast_away=0&timezone_offset=28800&dynamic_code=753347&country=CN&systemversion=8.0.0&devicemodle=SM-G9350&request_type=getIAPItemData"
#
# import json
#
# raw_dict = {}
# for item in a.split("&"):
#     data = item.split("=")
#     raw_dict[str(data[0])] = data[1]
# print(json.dumps(raw_dict))
#
# for key,value in raw_dict.items():
#     print(key, ":", value)
#

# import requests
#
# with requests.get("https://imyshare.com/hot-girl/") as session:
#   print(session.text)
#   page_html = etree.HTML(session.text)
#   src = page_html.xpath("/html/body/div[2]//@src")[0]
#   print(src)
import subprocess

fl_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "User-Agent": 'Mozilla/7.0 (compatible; ABrowse 0.4; Syllable)',
    "Remote Address": "206.119.79.46:443",
    "Referrer Policy": "strict-origin-when-cross-origin",
    "host": "fuliba2021.net"
}


def get_response(url):
    response = requests.get(url, headers=fl_headers, verify=False, timeout=3)
    response.close()
    return response.content


def get_rPic():
    # 获取页数
    page_url = "https://fuliba2021.net/flhz"
    print("get_rPic")
    res = get_response(page_url).decode()
    page_html = etree.HTML(res)
    # page = page_html.xpath("/html/body/section/div[1]/div/div[2]/ul/li[8]/span//text()")
    page = page_html.xpath("/html/body/section/div[1]/div/div[2]/ul/li[8]/span//text()")[0]
    print("page:", page)

    page_number = re.search("\d+", page).group()
    # print(page_number)

    pic_url = ""
    while pic_url == "":  # 有可能获取失败，2021016前面的都不行
        rand_page = random.randint(1, int(page_number))
        # 获取某一期
        index_url = "https://fuliba2021.net/flhz/page/" + str(rand_page)
        html = etree.HTML(get_response(index_url).decode())
        total = html.xpath("//article//h2//@href")
        rand_index = random.choice(total)
        # 获取页码
        page_index = \
            etree.HTML(get_response(rand_index).decode()).xpath("/html/body/section/div[1]/div/div[2]//text()")[-1]
        # print("----------", page_index, len(page_index))
        # 获取图片
        page_m = rand_index + "/" + page_index
        print("html:", page_m)
        pics = etree.HTML(get_response(page_m).decode())
        pics_xpath = pics.xpath("/html/body/section/div[1]/div/article/p[1]/img/@src")
        try:
            pic_url = random.choice(pics_xpath)
            print("pic_url:", pic_url)
        except:
            print("pic_url为空")
            print(pics_xpath)

        if pic_url != "":
            s = requests.get(pic_url, headers=fl_headers, verify=False, timeout=3)
            response_code = s.status_code
            result = s.url
            if str(result).endswith("FileDeleted") or str(result).endswith("101") or response_code != 200:
                pic_url = ""
                print("文件不存在，重新找")
                print(response_code)
    return pic_url

print(get_rPic())