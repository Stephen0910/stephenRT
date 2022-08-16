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

# from gevent import monkey
from concurrent.futures import ThreadPoolExecutor
import time

# monkey.patch_all(select=False)

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


async def version_max(a, b):
    """
    比较版本
    :param a: 新查询版本号
    :param b: 数据库中的版本
    :return:
    """
    if a == b:
        return False
    lista = str(a).split(".")
    listb = str(b).split(".")
    for index, i in enumerate(lista):
        if int(i) > int(listb[index]):
            return True


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
    except Exception as e:
        logger.error("sql执行失败：\n{0}\n{1}".format(str(e), sql))
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
    # logger.debug(url)
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
            try:
                rate = re.match("\d+.\d+", soup.find("div", {"itemprop": "starRating"}).text).group()
            except:
                rate = "人数过少，无评分"
            # version = re.search("\d+.\d+", re.search("\[\[\[\"\d+.\d+\"]]", response).group()).group()
            try:
                version = re.search("\d+.\d+.\d+.\d+|\d+.\d+.\d+|\d+.\d+",
                                    re.search("\[\[\[\"\d+.\d+.*?]],", response).group()).group()  # 2-4位版本号
                info = re.search("\[\[\[\d+,\".*?[0-9].[0-9]\"]]", response).group().split(",")
                sdk_version = [re.search("\d\d|\d.\d", x).group() for x in info]
                sdk_min = sdk_version[::2][-1]
                sdk_max = sdk_version[::2][0]
            except:
                # version = re.search("\d+.\d+.\d+", re.search("\[\[\[\"\d+.\d+.\d+\"]]", response).group()).group()  # 三位或四位
                version = "0.0"
                sdk_min = ""
                sdk_max = ""

    return {"name": name, "age": age, "recent_update": recent_update, "version": version, "rate": rate,
            "google_url": url, "gp_packageName": id, "sdk_min": sdk_min, "sdk_max": sdk_max}


async def asInfo(country, id):
    url = "https://apps.apple.com/{0}/app/id{1}".format(country,
                                                        id) if country != None else "https://apps.apple.com/app/id{0}".format(
        id)
    # logger.debug(url)

    con = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=con, trust_env=True) as session:
        async with session.get(url, proxy="http://127.0.0.1:7890") as resp:
            response = await resp.text(encoding="utf-8")
            soup = BeautifulSoup(response, "html.parser")
            name_info = soup.find(name="h1", attrs={"class": "product-header__title app-header__title"}).text.replace(
                " ",
                "").split(
                "\n")
            name, age = [x for x in name_info if len(x) > 0]
            update_date = soup.find(name="time", attrs={"data-test-we-datetime": ""}).text
            try:
                version = \
                    soup.find(name="p",
                              attrs={"class": "l-column small-6 medium-12 whats-new__latest__version"}).text.split(
                        " ")[
                        -1]
            except:
                logger.error("获取版本失败，可能是第一个版本")
                version = "0.0"
            rate = soup.find(name="span", attrs={"class": "we-customer-ratings__averages__display"}).text
            ver_infos = soup.find_all("div",
                                      {
                                          "class": "information-list__item l-column small-12 medium-6 large-4 small-valign-top"})

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


async def check_project(name, game_id, apple_country, as_id, gp_packageName, gp_version, as_version):
    msg = ""

    # 先处理GP
    if gp_packageName == None or gp_packageName == "":
        # logger.debug("没有谷歌包：{0}".format(name))
        pass
    else:
        try:
            gp_live = await gpInfo(gp_packageName)
            live_version = gp_live["version"]
            # logger.debug(name + ":" + live_version)

            if gp_version == None:
                # logger.debug("没有存:" + name)
                gp_version = "0.0"
            max_version = await version_max(live_version, gp_version)

            # 写入
            if max_version:
                timestamp = str(int(time.time()))
                game_package = gp_packageName
                gp_sql = """
                        INSERT INTO gp_version ( "game_id", "name", "age", "recent_update", "version", "rate", "google_url", "gp_packageName", "sdk_min", sdk_max, "timestamp")
VALUES	
({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', {8}, {9}, {10});""".format(game_id,
                                                                                  name.replace("\'", "\""),
                                                                                  gp_live["age"],
                                                                                  gp_live["recent_update"],
                                                                                  gp_live["version"],
                                                                                  gp_live["rate"],
                                                                                  gp_live["google_url"],
                                                                                  gp_live["gp_packageName"],
                                                                                  gp_live["sdk_min"],
                                                                                  gp_live["sdk_max"],
                                                                                  timestamp)

                msg = msg + "【{0}】 有更新 from GooglePlay\n版本:{1}||{3}\n{2}\n".format(name, gp_live["version"],
                                                                                 gp_live["google_url"], gp_version)
                await save_data(gp_sql)
                logger.debug(msg)

        except Exception as e:
            logger.debug("GP获取版本信息失败：{0}\n{1}".format(name, str(e)))

    # 处理iOS
    if as_id == None or as_id == "":
        # logger.debug("没有iOS包：{0}".format(name))
        pass
    else:
        try:
            as_live = await asInfo(country=apple_country, id=as_id)
            live_version = as_live["version"]
            # logger.debug(name + ":" + live_version)

            if as_version == None or as_version == "":
                # logger.debug("没有存:" + name)
                as_version = "0.0"
            max_version = await version_max(live_version, as_version)

            # 写入
            if max_version:
                timestamp = str(int(time.time()))
                as_sql = """
                    INSERT INTO as_version("game_id", "name", "age", "recent_update", "version", "rate", "version_info", "apple_url", "as_id", "timestamp")
VALUES
({0}, '{1}', '{2}', '{3}', '{4}', {5}, '{6}', '{7}', {8}, {9});""".format(game_id,
                                                                          str(as_live["name"].replace("\'", "\"")),
                                                                          as_live["age"],
                                                                          as_live["recent_update"],
                                                                          as_live["version"],
                                                                          as_live["rate"],
                                                                          json.dumps(as_live["version_info"]).replace(
                                                                              "\'",
                                                                              "\""),
                                                                          as_live["apple_url"], as_live["as_id"],
                                                                          timestamp)
                msg = msg + "【{0}】 有更新 from AppStore\n版本:{1}||{3}\n{2}\n".format(str(as_live["name"]),
                                                                               as_live["version"],
                                                                               as_live["apple_url"],
                                                                               as_version)

                await save_data(as_sql)
        except Exception as e:
            logger.debug("AS获取版本信息失败：{0}\n{1}".format(name, str(e)))



    return msg


async def search_all():
    app_sql = "SELECT * FROM game_info WHERE is_pulish is True"
    app_infos = await select_data(app_sql)
    names = [x["name"] for x in app_infos]
    gp_packageNames = [x["gp_packageName"] for x in app_infos]
    game_ids = [x["game_id"] for x in app_infos]
    apple_countrys = [x["apple_country"] for x in app_infos]
    as_ids = [x["as_id"] for x in app_infos]

    sql1 = "SELECT game_id,version FROM gp_version AS A WHERE NOT EXISTS (SELECT 1 FROM gp_version AS b WHERE b.game_id = A.game_id AND b.id > A.id )"
    sql2 = "SELECT game_id,version FROM as_version AS A WHERE NOT EXISTS (SELECT 1 FROM as_version AS b WHERE b.game_id = A.game_id AND b.id > A.id )"
    versions_sql1 = await select_data(sql1)
    versions_sql2 = await select_data(sql2)
    gp_versions, as_versions = {}, {}
    for index, i in enumerate(versions_sql1):
        gp_versions[i["game_id"]] = i["version"]
    for index, i in enumerate(versions_sql2):
        as_versions[i["game_id"]] = i["version"]

    tasks = []
    CONCURRENCY = 5
    semaphore = asyncio.Semaphore(CONCURRENCY)

    for index, name in enumerate(names):
        if game_ids[index] not in gp_versions.keys():
            gp_version = None
        else:
            gp_version = gp_versions[game_ids[index]]
        if game_ids[index] not in as_versions.keys():
            as_version = None
        else:
            as_version = as_versions[game_ids[index]]


        tasks.append(asyncio.ensure_future(
            check_project(name=name, game_id=game_ids[index], gp_packageName=gp_packageNames[index], apple_country=apple_countrys[index],
                          as_id=as_ids[index], gp_version=gp_version, as_version=as_version)))

    msg = await asyncio.gather(*tasks)
    return msg


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    gp_package = "eightball.pool.live.eightballpool.billiards"
    # result = loop.run_until_complete(gpInfo(gp_package))

    result = loop.run_until_complete(search_all())

    # result = loop.run_until_complete(asInfo("cn", "1517576080"))
    loop.close()
    print(result)
