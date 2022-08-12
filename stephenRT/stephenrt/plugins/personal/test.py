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
import re, random, datetime

k_url = "https://act.quark.cn/apps/qknewshours/routes/hot_news"
base_url = "https://iflow.uc.cn/webview/news?app=&aid="
base = "https://iflow.uczzd.cn/iflow/api/v1/article/aggregation?__t=1659609915000&aggregation_id=16665090098771297825&count=50"

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

u_headers = {
    'authority': 'iflow.uc.cn',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
    'cache-control': 'max-age=0',
    'cookie': '__wpkreporterwid_=93d89238-09f4-4e51-bd55-77dbfee29f9b; cna=Qu0tGxxCmlgCAavdkbRFoQG9; ctoken=Ldk13z9-eEpjBsZiYAdyXiqc; sn=adfca447-bc88-4a55-aad2-ca314a28af79; isg=BHh4lZtWbiuax4K0F8Prw9ZhSSYK4dxr1fjDZrLpybNmzRi3WvRy-xHvgcX9m5RD',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

link = "https://iflow-news.quark.cn/r/quark-iflow?&item_id="


def news_list():
    with requests.get(url=k_url, headers=k_headers) as session:
        soup = BeautifulSoup(session.content, "html.parser")
        all_contents = soup.find_all("div", attrs={"class": "rax-view-v2 aiticle-list-box"})  # 所有内容
        times_soup = all_contents[0].find_all(name="div", attrs={"class": "rax-view-v2 date"})
        some = all_contents[0].find_all(name="div", attrs={"data-c": "news"})
        news = [x["data-exposure-extra"] for x in some]
        every = all_contents[0].find_all(name="div",
                                         attrs={"class": "rax-view-v2 article-item-inner-text graphics-mode"})
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

        urls = [base_url + id for id in ids]
        for url in urls:
            print(url)


"""
new
"""

from bs4 import BeautifulSoup
import urllib

payload={}
s_headers1 = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
  'Cache-Control': 'max-age=0',
  'Connection': 'keep-alive',
  'Cookie': 'IPLOC=CN5101; SUID=757D58DA364A910A0000000062AAA554; SUV=1655350614089929; ssuid=837765834; sw_uuid=8828784640; ABTEST=1|1659670966|v1; weixinIndexVisited=1; ld=fyllllllll2AEJXwlllllpa7utklllll$dLQ1Zllll9lllllxylll5@@@@@@@@@@; LCLKINT=2626; LSTMV=210%2C72; SNUID=026A4FC21812F2D3D5DC8A5618999969; JSESSIONID=aaa0ICKmz5eXX5xTbAzjy; ariaDefaultTheme=undefined',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'none',
  'Sec-Fetch-User': '?1',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
  'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"'
}

s_headers2 = {
  'authority': 'mp.weixin.qq.com',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'accept-language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
  'cache-control': 'max-age=0',
  'cookie': 'RK=QcOsQQ7xYJ; ptcz=fd9af81554cc3f6f5c3876beea21d67e4df9fda8632d228c28976a44c9a0705f; tvfe_boss_uuid=ff47cfc1329a5325; pgv_pvid=9212904821; fqm_pvqid=34f4b83f-73b4-4640-b8e1-8e9f2e00b8b0; pac_uid=0_c5d044dc9edfb; _ga=GA1.2.771449081.1656559089; _hjSessionUser_2765497=eyJpZCI6IjBiZDczNWZlLTE1MDctNTA5ZC1hN2EwLTg1ZDg5OWEzYWY4NCIsImNyZWF0ZWQiOjE2NTY1NTkwNzc1MDQsImV4aXN0aW5nIjp0cnVlfQ==; _tc_unionid=3d5869bb-ed10-4e4d-9992-c267f2c5c3dc; ua_id=Jl3o4YHGbRLnFjE7AAAAAFmattsrPSp13frIRDxDUcw=; mm_lang=zh_CN; ts_uid=9923057400; rand_info=CAESIEd0yUcSLhRv5bFw1zH/DynWWI8uDYL3tOqWyvoj4RSa; slave_bizuin=3893097792; data_bizuin=3893097792; bizuin=3893097792; data_ticket=iSHBnh8qaTMCimQO9QPI4DCcgA+wCL2CHCPe4L2btii19UbxKMG46Uq60MkZzf9w; slave_sid=RW9jdnpFQVZmTk51TWhIaFBURkw0aXpnRk9CWGV5UjZjUW8wNWZVbWdpamdYUVJfb2hZaVFtbk9EODY1OFhwYUVMc1FTZV9CRGJaWDFIb0w4enM3bjA4TXRJUnlFZzd1WFgwemRmS0hUc0dMcGk5T1JEVk5ORkI1V3N2SEJ4MUc4akhyWVlxUFpLYmpmT1lM; slave_user=gh_9a01da528413; xid=ed8acd368a4f9b2d6dc7fc009e2f3984; rewardsn=; wxtokenkey=777; wwapp.vid=; wwapp.cst=; wwapp.deviceid=; rewardsn=; wxtokenkey=777',
  'if-modified-since': 'Wed, 10 Aug 2022 14:05:42 +0800',
  'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}

def get_biz(name):
    sogou_url = "https://weixin.sogou.com/weixin?type=1&s_from=input&query="
    with requests.get(sogou_url+name, headers=s_headers1, data=payload) as session:
        soup = BeautifulSoup(session.content, "html.parser")

        data = soup.find(name="a", attrs={"target": "_blank", "uigs": "account_article_0"})
        id_url = "https://weixin.sogou.com" + data["href"]

        print(id_url)





    with requests.get(id_url, headers=s_headers2, data=payload) as session:
        soup = BeautifulSoup(session.content, "html.parser")
        print("soup:", soup)
        data = soup.find(name="body", attrs={"id": "activity-detail"})
        print(data)

    url = "https://mp.weixin.qq.com/s?src=11&timestamp=1660111536&ver=3973&signature=PX89b35JyrLT0HQ70xysmpiRVR7fIQ0LT6SdmWfpQxgMVJnmrHwOyENSqVh1mt8BwQwwDE5iP0Dp7VfDZV4Me8tkv1jEcaQaJc3yL5z3UoM198qryzqAAVfwPJFfjVCW&new=1"




    # response = requests.request("GET", new_url, headers=headers, data=payload)

    # print(response.text)


a = get_biz("成都发布")
print(a)