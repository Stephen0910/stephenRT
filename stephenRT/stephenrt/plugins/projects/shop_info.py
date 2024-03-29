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
import logzero, logging
from logzero import logger

logzero.loglevel(logging.DEBUG)
import socks
import socket

logger.debug("设置完毕")

if __name__ == '__main__':
    import stephenRT.stephenrt.privateCfg as cfg
else:
    import stephenrt.privateCfg as cfg

pgsql = cfg.config_content

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
    with requests.get(url, headers=gp_headers, data=payload, proxies=proxies) as session:

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


async def get_size(id):
    url = f"https://apksos.com/app/{id}"
    with requests.get(url) as session:
        response = session.text
        soup = BeautifulSoup(response, "html.parser")
        data = soup.find("button", {"class": "primary"}).text
        size = re.search("\d+.\d+MB", data).group()
        version = soup.find("ul", {"class": "list-unstyled"}).text.split(" ")[2]
        # version = re.search("Version:.*?\d<", version)
        logger.debug(size)
        logger.debug(version)
        return [version, size]


async def gpInfo(id):
    url = "https://play.google.com/store/apps/details?id=" + id
    # logger.debug(url)
    con = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=con, trust_env=True) as session:
        async with session.get(url, proxy="http://127.0.0.1:7890") as resp:
            response = await resp.text(encoding="utf-8")

            soup = BeautifulSoup(response, "html.parser")
            name = soup.find("h1", {"itemprop": "name"}).text
            # logger.debug(name)
            age = soup.find("span", {"itemprop": "contentRating"}).text
            icon = soup.find("img", {"class": "T75of cN0oRe fFmL2e"})["src"]
            download = [x.text for x in soup.find_all("div", {"class": "ClM7O"})]
            # print(download)
            recent_update = soup.find("div", {"class": "xg1aie"}).text
            try:
                rate = re.match("\d+.\d+", soup.find("div", {"itemprop": "starRating"}).text).group()
            except:
                rate = 0
            # version = re.search("\d+.\d+", re.search("\[\[\[\"\d+.\d+\"]]", response).group()).group()
            try:
                version = re.search("\d+.\d+.\d+.\d+|\d+.\d+.\d+|\d+.\d+",
                                    re.search("\[\[\[\"\d+\.\d+.*?]],", response).group()).group()  # 2-4位版本号
                # version = re.search("\[\[\[\"\d+\.\d+", response).group()
                info = re.search("\[\[\[\d+,\".*?[0-9].[0-9]\"]]", response).group().split(",")
                sdk_version = [re.search("\d\d|\d.\d", x).group() for x in info]
                sdk_min = sdk_version[::2][-1]
                sdk_max = sdk_version[::2][0]
            except Exception as e:
                logger.error(f"{id} {name}: {str(e)}")
                # version = re.search("\d+.\d+.\d+", re.search("\[\[\[\"\d+.\d+.\d+\"]]", response).group()).group()  # 三位或四位
                version = "0.0"
                sdk_min = ""
                sdk_max = ""
            logger.debug(version)

    # 获取size -  影响速度
    # size_data = await get_size(id=id)
    # if size_data[0] == str(version):
    #     size = size_data[1]
    # else:
    #     size = "0"

    result = {"name": name, "age": age, "recent_update": recent_update, "version": version, "rate": rate,
              "google_url": url, "gp_packageName": id, "sdk_min": sdk_min, "sdk_max": sdk_max, "icon": icon}

    return result


import google_play_scraper


async def gp_info_new(id):
    socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 7891)
    socket.socket = socks.socksocket
    app = google_play_scraper.app(id)
    return app


async def asInfo(country, id):
    """
    api: https://itunes.apple.com/lookup?id=1330550298
    :param country:
    :param id:
    :return:
    """

    url = "https://apps.apple.com/{0}/app/id{1}".format(country,
                                                        id) if country != None else "https://apps.apple.com/app/id{0}".format(
        id)
    # logger.debug(url)
    con = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=con, trust_env=True) as session:
        # async with session.get(url, proxy="http://127.0.0.1:7890") as resp:
        async with session.get(url) as resp:
            response = await resp.text(encoding="utf-8")
            soup = BeautifulSoup(response, "html.parser")
            name_info = soup.find(name="h1", attrs={"class": "product-header__title app-header__title"}).text.replace(
                "  ",
                "").split(
                "\n")
            name, age = [x for x in name_info if len(x) > 0]
            update_date = soup.find(name="time", attrs={"data-test-we-datetime": ""}).text
            icon = soup.find(name="source", attrs={"type": "image/png"})["srcset"].split(" ")[0]
            try:
                version = \
                    soup.find(name="p",
                              attrs={"class": "l-column small-6 medium-12 whats-new__latest__version"}).text.split(
                        " ")[
                        -1]
            except Exception as e:
                print("AS获取版本失败，可能是第一个版本:{0}, {1}: {2}".format(name, url, str(e)))  # logger有bug
                version = "0.0"
            rate = soup.find(name="span", attrs={"class": "we-customer-ratings__averages__display"}).text
            ver_infos = soup.find_all("div",
                                      {
                                          "class": "information-list__item l-column small-12 medium-6 large-4 small-valign-top"})

            verInfo_dict = {}
            for info in ver_infos:
                each_info = [x for x in info.text.replace("  ", "").split("\n") if len(x) > 0]
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

    result = {"name": name, "age": age, "recent_update": update_date, "version": version, "rate": rate,
              "version_info": verInfo_dict, "apple_url": url, "as_id": id, "icon": icon}
    # logger.debug(result)
    return result


async def check_project(name, game_id, apple_country, as_id, gp_packageName, gp_version, as_version):
    msg = ""

    # 先处理GP
    if gp_packageName == None or gp_packageName == "":
        # logger.debug("没有谷歌包：{0}".format(name))
        pass
    else:
        # 直接使用接口
        gp_live = await gp_info_new(gp_packageName)
        logger.debug(f"gp_live: {json.dumps(gp_live)}")
        try:
            live_version = gp_live["version"]
        except Exception as e:
            logger.error(f"{name} 获取gp version 失败: {e}")

        if gp_version == None:
            gp_version == "0.0"  # 第一个版本
        max_version = await version_max(live_version, gp_version)
        logger.debug(max_version)
        if max_version:
            logger.debug(f"{name} gp发现新版本 {live_version}")
            gp_sql = f"""INSERT INTO gp_version ("apple_id", "title", "realInstalls", "score", "inAppProductPrice", "genre",
             "icon", "contentRating", "released", "updated", "version", "url")
            VALUES {gp_live["apple_id"], gp_live["title"], gp_live["realInstalls"], gp_live["score"], gp_live[
                "inAppProductPrice"], gp_live["genre"], gp_live["icon"], gp_live["contentRating"],
                    gp_live["released"],
                    gp_live["updated"], gp_live["version"], gp_live["url"]};"""
            logger.debug(gp_sql)

            # 获取差别
            logger.debug(json.dumps(gp_live))
            diff_msg = ""
            diff_sql = f'SELECT * FROM gp_version WHERE game_id = {game_id} ORDER BY "version" DESC limit 1'
            sql_result = await select_data(diff_sql)
            logger.debug(sql_result[0])
            logger.debug(type(sql_result[0]))
            result = dict(sql_result[0])
            for key in gp_live.keys():
                logger.debug(f"{key}")
                logger.debug(f"{result[key]}, {gp_live[key]}")
                if str(result[key]) != str(gp_live[key]) and key != "version":
                    diff_msg = diff_msg + f"{key} diff: {gp_live[key]} | {result[key]} \n"

            msg = msg + "【{0}】 有更新 from GooglePlay\n版本:{1}||{3}\n{2}\n".format(gp_live["name"], gp_live["version"],
                                                                               gp_live["google_url"], gp_version)
            msg = msg + diff_msg
            # await save_data(gp_sql)
            logger.debug(msg)

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
                logger.info(str(max_version) + ": " + name)
                timestamp = str(int(time.time()))
                as_sql = """
                    INSERT INTO as_version("game_id", "name", "age", "recent_update", "version", "rate", "version_info", "apple_url", "as_id", "timestamp", "icon")
VALUES
({0}, '{1}', '{2}', '{3}', '{4}', {5}, '{6}', '{7}', {8}, {9}, '{10}');""" \
                    .format(game_id,
                            str(as_live["name"].replace("\'",
                                                        "\"")),
                            as_live["age"],
                            as_live["recent_update"],
                            as_live["version"],
                            as_live["rate"],
                            json.dumps(
                                as_live["version_info"]).replace(
                                "\'",
                                "\""),
                            as_live["apple_url"],
                            as_live["as_id"],
                            timestamp,
                            as_live["icon"])

                # 获取差别
                logger.debug(json.dumps(as_live))
                diff_msg = ""
                diff_sql = f'SELECT * FROM as_version WHERE game_id = {game_id} ORDER BY "version" DESC limit 1'
                sql_result = await select_data(diff_sql)
                logger.debug(sql_result[0])
                logger.debug(type(sql_result[0]))
                result = dict(sql_result[0])
                for key in as_live.keys():
                    logger.debug(f"{key}")
                    logger.debug(f"{result[key]}, {as_live[key]}")
                    if str(result[key]) != str(as_live[key]) and key != "version":
                        diff_msg = diff_msg + f"{key} diff: {as_live[key]} | {result[key]} \n"

                msg = msg + "【{0}】 有更新 from AppStore\n版本:{1}||{3}\n{2}\n".format(str(as_live["name"]),
                                                                                 as_live["version"],
                                                                                 as_live["apple_url"],
                                                                                 as_version)
                msg = msg + diff_msg
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
    logger.debug(gp_versions)
    logger.debug(as_versions)
    tasks = []
    # CONCURRENCY = 10
    # semaphore = asyncio.Semaphore(CONCURRENCY)
    msg = ""
    from multiprocessing.dummy import Pool
    pool = Pool(4)
    for index, name in enumerate(names):
        # logger.debug(f"{index} {name}")
        if game_ids[index] not in gp_versions.keys():
            gp_version = None
        else:
            gp_version = gp_versions[game_ids[index]]
        if game_ids[index] not in as_versions.keys():
            as_version = None
        else:
            as_version = as_versions[game_ids[index]]

        # tasks.append(asyncio.ensure_future(
        #     check_project(name=name, game_id=game_ids[index], gp_packageName=gp_packageNames[index],
        #                   apple_country=apple_countrys[index],
        #                   as_id=as_ids[index], gp_version=gp_version, as_version=as_version)))
        # single_msg = await check_project(name=name, game_id=game_ids[index], gp_packageName=gp_packageNames[index],
        #                            apple_country=apple_countrys[index],
        #                            as_id=as_ids[index], gp_version=gp_version, as_version=as_version)
        args = (name, game_ids[index], gp_packageNames[index],apple_countrys[index], as_ids[index], gp_version, as_version)
        pool.map(check_project, list(args))

    # msg = await asyncio.gather(*tasks)
    return msg


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    #
    #
    gp_package = "slots.machine.winning.android"
    gp_package1 = "candy.craze.match3.free.android"
    country = ""
    as_id = 1521595172

    # result = loop.run_until_complete(gp_info_new(gp_package1))
    # print(result)
    # result1 = loop.run_until_complete(asInfo(country, as_id))
    # print(result1)
    result = loop.run_until_complete(search_all())
    loop.close()
    # socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 7891)
    # socket.socket = socks.socksocket
    #
    # from google_play_scraper import app
    #
    # app = app(gp_package)
    # print(json.dumps(app))
