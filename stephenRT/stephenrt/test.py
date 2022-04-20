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
import requests, json, random, time
from lxml import etree
import re

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "Remote Address": "206.119.79.46:443"
}

def get_response(url):
    response = requests.get(url, headers=headers)
    response.close()
    return response.content


def get_rPic():
    # 获取页数
    page_url = "https://fuliba2021.net/flhz/page/1"
    page_html = etree.HTML(get_response(page_url).decode())
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
        page_index = etree.HTML(get_response(rand_index).decode()).xpath("/html/body/section/div[1]/div/div[2]//text()")[-1]
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
            s = requests.get(pic_url)
            response_code = s.status_code
            result = s.url
            if str(result).endswith("FileDeleted") or str(result).endswith("101") or response_code != 200:
                pic_url = ""
                print("文件不存在，重新找")
                print(response_code)
        pic_url = ""
    return pic_url


#
# f = "https://tvax4.sinaimg.cn/large/718153f4gy1gxx0cvcmrsg20a5053k5o.gif"
#
# s = requests.get(f)
# #
# print(s.status_code)
# print(s.url)
# s.close()

get_rPic()