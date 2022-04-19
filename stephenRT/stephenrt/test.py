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
import requests,json, random
from lxml import etree
import re


def get_response(url):
    response = requests.get(url)
    response.close()
    return response.content


def get_rPic():
    # 获取页数
    page_url = "https://fuliba2021.net/flhz"
    page_html = etree.HTML(get_response(page_url).decode())
    page = page_html.xpath("/html/body/section/div[1]/div/div[2]/ul/li[8]/span//text()")[0]
    page_number = re.search("\d+", page).group()
    print(page_number)
    rand_page = random.randint(1, int(page_number))
    # 获取某一期
    index_url = "https://fuliba2021.net/flhz/page/" + str(rand_page)
    html = etree.HTML(get_response(index_url).decode())
    total = html.xpath("//article//h2//@href")
    rand_index = random.choice(total)
    print(rand_index)
    # 获取图片
    page3 = rand_index + "/3"
    pics = etree.HTML(get_response(page3).decode())
    pics_xpath = pics.xpath("/html/body/section/div[1]/div/article/p[1]/img/@src")
    pic_url = random.choice(pics_xpath)
    return pic_url



get_rPic()