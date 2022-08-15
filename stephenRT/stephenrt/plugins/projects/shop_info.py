#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/8/11 15:31
# @Author   : StephenZ
# @Site     : 
# @File     : shop_info.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

from gevent import monkey

monkey.patch_all(select=False)

import aiohttp

import requests, json, re, httpx
from bs4 import BeautifulSoup
import asyncpg
import asyncio
import stephenrt.privateCfg as cfg
pgsql = cfg.config_content
import grequests

import logzero, logging
from logzero import logger

logzero.loglevel(logging.DEBUG)

gp_headers = {
    'authority': 'api.qimai.cn',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
    'cookie': 'Hm_lvt_ff3eefaf44c797b33945945d0de0e370=1660202726; qm_check=SxJXQEUSChd2fHd1dRQQd19fV1xVHBVhR1xSUVoYAR4CHgAQGGZAW1ZNY1xZVFVCEHRVRlxUVxARY0FaSlVCXxkQGAVPAgAJAHcIdHUZGRwQY0JeVERqWFVcVUIQVEJZRlBFGxIVEldQVVNbEgoSABkHHgAVABgIEk0%3D; PHPSESSID=o5hiuejq879t7odnte3tfaouai; gr_user_id=e5086f07-2eed-4607-b005-d5d6565c1260; ada35577182650f1_gr_session_id=e94432aa-6215-4374-ad90-3f60103c9b39; ada35577182650f1_gr_session_id_e94432aa-6215-4374-ad90-3f60103c9b39=true; tgw_l7_route=29ef178f2e0a875a4327cbfe5fbcff7e; synct=1660202781.432; syncd=-564; Hm_lpvt_ff3eefaf44c797b33945945d0de0e370=1660202782; PHPSESSID=bmip6o4loq8prqjue59fts7ken',
    'origin': 'https://www.qimai.cn',
    'referer': 'https://www.qimai.cn/',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
}


async def select_data(sql):
    conn = await asyncpg.connect(user=pgsql["user"], password=pgsql["password"], database=pgsql["database"],
                                 host=pgsql["host"])
    data = await conn.fetch(sql)
    await conn.close()
    return data


async def save_data(sql):
    """
    异步执行插入sql
    :param sql:
    :return:
    """
    conn = await asyncpg.connect(user=pgsql["user"], password=pgsql["password"], database=pgsql["database"],
                                 host=pgsql["host"])
    # print("conn:", conn)

    try:
        await conn.execute(sql)
    except:
        logger.error(sql)
    await conn.close()


async def asInfo_abundon(country, id):
    proxies = {"http": "127.0.0.1:7890", "https": "127.0.0.1:7890"}
    payload = {}

    url = "https://apps.apple.com/{0}/app/id{1}".format(country,
                                                        id) if country != None else "https://apps.apple.com/app/id{0}".format(
        id)
    logger.debug(url)

    # with requests.get(url, headers=headers, data=payload, proxies=proxies) as session:
    with grequests.get(url, headers=gp_headers, data=payload, proxies=proxies) as session:

        response = session.content
    soup = BeautifulSoup(response, "html.parser")
    name_info = soup.find(name="h1", attrs={"class": "product-header__title app-header__title"}).text.replace(" ",
                                                                                                              "").split(
        "\n")
    name, age = [x for x in name_info if len(x) > 0]
    update_date = soup.find(name="time", attrs={"data-test-we-datetime": ""}).text
    try:
        version = \
            soup.find(name="p", attrs={"class": "l-column small-6 medium-12 whats-new__latest__version"}).text.split(
                " ")[
                -1]
    except:
        logger.error("获取版本失败，可能是第一个版本")
        version = "0.0.0"
    rate = soup.find(name="span", attrs={"class": "we-customer-ratings__averages__display"}).text
    ver_infos = soup.find_all("div",
                              {"class": "information-list__item l-column small-12 medium-6 large-4 small-valign-top"})

    verInfo_dict = {}
    for info in ver_infos:
        each_info = [x for x in info.text.replace(" ", "").split("\n") if len(x) > 0]
        base_value = each_info[1:]
        if len(base_value) == 1:
            verInfo_dict[each_info[0]] = each_info[1]
        elif len(base_value) % 2 == 1:
            verInfo_dict[each_info[0]] = base_value
        else:
            new_dic = {}
            for index, i in enumerate(base_value):
                if index % 2 == 0:
                    new_dic[i] = base_value[index + 1]
            verInfo_dict[each_info[0]] = new_dic
    return {"name": name, "age": age, "recent_update": update_date, "version": version, "rate": rate,
            "version_info": verInfo_dict, "apple_url": url, "as_id": id}


async def gpInfo_aboundon(id):
    url = "https://play.google.com/store/apps/details?id=" + id
    proxies = {"http": "127.0.0.1:7890", "https": "127.0.0.1:7890"}
    logger.debug(url)
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
        'user-agent': 'Mozilla/4.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }

    try:
        with requests.get(url, headers=headers, data=payload, proxies=proxies) as session:
            response = session.text
    except Exception as e:
        logger.error("获取信息失败: {0}".format(str(e)))
        return
    soup = BeautifulSoup(response, "html.parser")
    name = soup.find("h1", {"itemprop": "name"}).text
    age = soup.find("span", {"itemprop": "contentRating"}).text

    download = [x.text for x in soup.find_all("div", {"class": "ClM7O"})]
    # print(download)
    recent_update = soup.find("div", {"class": "xg1aie"}).text
    rate = re.match("\d+.\d+", soup.find("div", {"itemprop": "starRating"}).text).group()

    # version = re.search("\d+.\d+", re.search("\[\[\[\"\d+.\d+\"]]", response).group()).group()
    try:
        version = re.search("\d+.\d+", re.search("\[\[\[\"\d+.\d+\"]]", response).group()).group()  # 两位版本号
    except:
        version = re.search("\d+.\d+.\d+", re.search("\[\[\[\"\d+.\d+.\d+\"]]", response).group()).group()  # 三位
    info = re.search("\[\[\[\d+,\".*?[0-9].[0-9]\"]]", response).group().split(",")
    sdk_version = [re.search("\d\d|\d.\d", x).group() for x in info]
    sdk_min = sdk_version[::2][-1]
    sdk_max = sdk_version[::2][0]

    return {"name": name, "age": age, "recent_update": recent_update, "version": version, "rate": rate,
            "google_url": url, "gp_packageName": id, "sdk_min": sdk_min, "sdk_max": sdk_max}


async def gpInfo(id):
    url = "https://play.google.com/store/apps/details?id=" + id
    con = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=con, trust_env=True) as session:
        async with session.get(url, proxy="http://127.0.0.1:7890") as resp:
            response = await resp.text(encoding="utf-8")

            soup = BeautifulSoup(response, "html.parser")
            name = soup.find("h1", {"itemprop": "name"}).text
            age = soup.find("span", {"itemprop": "contentRating"}).text

            download = [x.text for x in soup.find_all("div", {"class": "ClM7O"})]
            # print(download)
            recent_update = soup.find("div", {"class": "xg1aie"}).text
            rate = re.match("\d+.\d+", soup.find("div", {"itemprop": "starRating"}).text).group()

            # version = re.search("\d+.\d+", re.search("\[\[\[\"\d+.\d+\"]]", response).group()).group()
            try:
                version = re.search("\d+.\d+", re.search("\[\[\[\"\d+.\d+\"]]", response).group()).group()  # 两位版本号
            except:
                version = re.search("\d+.\d+.\d+", re.search("\[\[\[\"\d+.\d+.\d+\"]]", response).group()).group()  # 三位
            info = re.search("\[\[\[\d+,\".*?[0-9].[0-9]\"]]", response).group().split(",")
            sdk_version = [re.search("\d\d|\d.\d", x).group() for x in info]
            sdk_min = sdk_version[::2][-1]
            sdk_max = sdk_version[::2][0]

    return {"name": name, "age": age, "recent_update": recent_update, "version": version, "rate": rate,
            "google_url": url, "gp_packageName": id, "sdk_min": sdk_min, "sdk_max": sdk_max}


async def asInfo(country, id):
    proxies = {"http": "127.0.0.1:7890", "https": "127.0.0.1:7890"}
    payload = {}

    url = "https://apps.apple.com/{0}/app/id{1}".format(country,
                                                        id) if country != None else "https://apps.apple.com/app/id{0}".format(
        id)
    logger.debug(url)

    con = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=con, trust_env=True) as session:
        async with session.get(url, proxy="http://127.0.0.1:7890") as resp:
            response = await resp.text(encoding="utf-8")
            soup = BeautifulSoup(response, "html.parser")
            name_info = soup.find(name="h1", attrs={"class": "product-header__title app-header__title"}).text.replace(" ",
                                                                                                                      "").split(
                "\n")
            name, age = [x for x in name_info if len(x) > 0]
            update_date = soup.find(name="time", attrs={"data-test-we-datetime": ""}).text
            try:
                version = \
                    soup.find(name="p", attrs={"class": "l-column small-6 medium-12 whats-new__latest__version"}).text.split(
                        " ")[
                        -1]
            except:
                logger.error("获取版本失败，可能是第一个版本")
                version = "0.0.0"
            rate = soup.find(name="span", attrs={"class": "we-customer-ratings__averages__display"}).text
            ver_infos = soup.find_all("div",
                                      {"class": "information-list__item l-column small-12 medium-6 large-4 small-valign-top"})

            verInfo_dict = {}
            for info in ver_infos:
                each_info = [x for x in info.text.replace(" ", "").split("\n") if len(x) > 0]
                base_value = each_info[1:]
                if len(base_value) == 1:
                    verInfo_dict[each_info[0]] = each_info[1]
                elif len(base_value) % 2 == 1:
                    verInfo_dict[each_info[0]] = base_value
                else:
                    new_dic = {}
                    for index, i in enumerate(base_value):
                        if index % 2 == 0:
                            new_dic[i] = base_value[index + 1]
                    verInfo_dict[each_info[0]] = new_dic
    return {"name": name, "age": age, "recent_update": update_date, "version": version, "rate": rate,
            "version_info": verInfo_dict, "apple_url": url, "as_id": id}




if __name__ == '__main__':
    # name = "clubillion"
    # country = apps[name]["country"]
    # apple_id = apps[name]["apple_id"]
    # b = asInfo(country, apple_id)
    # print(json.dumps(b))
    # b = json.dumps(gpInfo(apps[name]["google_id"]))
    # print(b)
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(main("endless.nightmare.shrine.horror.scary.free.android"))
    # result = loop.run_until_complete(asInfo("ca", "1472473722"))
    loop.close()
    print(json.dumps(result))
