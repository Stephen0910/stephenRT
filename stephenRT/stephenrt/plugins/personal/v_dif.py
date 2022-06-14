#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/6/8 15:54
# @Author   : StephenZ
# @Site     : 
# @File     : v_dif.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>
from lxml import etree
import requests

linhunyun = "https://api.linhun.vip/api/Littlesistervideo?type=json"  # linhunyun
hot_girl = "https://imyshare.com/hot-girl"
qiqu = "http://tool.qiquhao.com/jsdy/"
suiji = "https://jiejie.de/xjj//get/get0.php"
suiji1 = "https://mm.diskgirl.com/get/get1.php"


hot_headers = {
    "cookie": "_ga=GA1.2.409272992.1654657681; _gid=GA1.2.19552097.1654657681; csrftoken=mbIbZueOzEtVkuhQyjvwMrwC8ie5oj8qfSZV8ChtKT9OnYAKY53NvpiNM3Mkhi6y; ShareID=s1livl5e1zmwrhj2fu8vmgitkda11j05; article_4_read=True; article_45_read=True; _gat_gtag_UA_165677247_1=1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
    }
with requests.get(hot_girl, headers=hot_headers) as session:

    print(session.text)
    page_html = etree.HTML(session.text)
    src = page_html.xpath("/html/body/div[2]//@src")[0]
    print(src)