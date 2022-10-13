#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/10/11 10:40
# @Author   : StephenZ
# @Site     : 
# @File     : live_info.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import json, requests
import asyncpg
import asyncio
from google_play_scraper import app
import logzero, logging
from logzero import logger

if __name__ == '__main__':
    from local_config import *
else:
    from .local_config import *
import time
from timeit import default_timer as timer
import aiohttp
from bs4 import BeautifulSoup
import psycopg2, psycopg2.extras
from psycopg2.extras import RealDictCursor
from multiprocessing.dummy import Pool
import json_tools

logzero.loglevel(logging.DEBUG)

import socks
import socket

thread_num = 50
pool = Pool(thread_num)


def filter_values(value):
    if isinstance(value, list):
        return list(map(filter_values, value))
    if isinstance(value, dict):
        return {k: filter_values(v) for k, v in value}
    if isinstance(value, str):
        stripped = value.strip().replace('\\u0000', '').replace('\u0000', '').replace(u'\u0000', '')
        while '\\-' in stripped:
            stripped = stripped.replace('\\-', '-')
        while '\\+' in stripped:
            stripped = stripped.replace('\\+', '+')
        while '\\E' in stripped:
            stripped = stripped.replace('\\E', 'E')
        while '\\&' in stripped:
            stripped = stripped.replace('\\&', '&')
        return stripped
    return value

def version_max(a, b):
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


def select_data(sql):
    # conn = psycopg2.connect(user=pgsql["user"], password=pgsql["password"], database=pgsql["database"],
    #                              host=pgsql["host"])
    with psycopg2.connect(user=pgsql["user"], password=pgsql["password"], database=pgsql["database"],
                          host=pgsql["host"]) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql)
            data = cursor.fetchall()
    return data


def save_data(sql):
    """
    异步执行插入sql
    :param sql:
    :return:
    """
    with psycopg2.connect(user=pgsql["user"], password=pgsql["password"], database=pgsql["database"],
                          host=pgsql["host"]) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            # data = conn.fetch(sql)
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                logger.error("sql执行失败：\n{0}\n{1}".format(str(e), sql))


def app_google(gp_package):
    socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 7891)
    socket.socket = socks.socksocket
    # logger.debug("代理设置完成")
    app_info = app(gp_package)
    # logger.debug(app_info)
    return app_info


def app_apple(country, id):
    """
    api: https://itunes.apple.com/lookup?id=1330550298
    :param country:
    :param id:
    :return:
    """
    # socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 7891)
    # socket.socket = socks.socksocket

    url = "https://apps.apple.com/{0}/app/id{1}".format(country,
                                                        id) if country != None else "https://apps.apple.com/app/id{0}".format(
        id)
    # logger.debug(url)
    # con = aiohttp.TCPConnector(ssl=False)
    # async with aiohttp.ClientSession(connector=con, trust_env=True) as session:
    with requests.get(url) as resp:
        # async with session.get(url, proxy="http://127.0.0.1:7891") as resp:
        response = resp.text
        # logger.debug(response)
        soup = BeautifulSoup(response, "html.parser")
        name_info = soup.find(name="h1", attrs={"class": "product-header__title app-header__title"}).text.replace(
            "  ",
            "").split(
            "\n")
        name, age = [x for x in name_info if len(x) > 0]
        update_date = soup.find(name="time", attrs={"data-test-we-datetime": ""}).text
        try:
            rank = soup.find(name="a", attrs={"class": "inline-list__item"}).text.strip()
            rank = re.search("\d+", rank).group()
        except:
            rank = ""
        # logger.debug(rank)
        icon = soup.find(name="source", attrs={"type": "image/png"})["srcset"].split(" ")[0]
        try:
            version = \
                soup.find(name="p",
                          attrs={"class": "l-column small-6 medium-12 whats-new__latest__version"}).text.split(
                    " ")[
                    -1]
        except Exception as e:
            version = ""
            logger.warning("AS获取版本失败，可能是第一个版本:{0}, {1}: {2} 重置: {3}".format(name, url, str(e), version))  # logger有bug

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
    verInfo_dict = filter_values(json.dumps(verInfo_dict).replace("'", "&#39;").replace("\\xa0", " "))
    result = {"name": name, "age": age, "recent_update": update_date, "version": version, "rate": rate,
              "version_info": verInfo_dict, "apple_url": url, "as_id": id, "icon": icon, "rank": rank}
    # logger.debug(f"apple_info: {result}")
    return result


def check_project(game_id):
    time1 = timer()
    msg = ""
    # 根据game_id 获取相关信息
    game_sql = f'SELECT * FROM "game_info" WHERE game_id = {game_id}'
    result = select_data(game_sql)
    project_info = result[0]
    # logger.debug(project_info)
    apple_country = project_info["apple_country"]
    as_id = project_info["as_id"]
    apple_country = project_info["apple_country"]
    gp_packageName = project_info["gp_packageName"]
    name = project_info["name"]
    # 获取gp_version
    # version_sql1 = f"SELECT game_id,version FROM gp_version AS A WHERE NOT EXISTS (SELECT 1 FROM gp_version AS b WHERE b.game_id = A.game_id AND b.id > A.id ) and game_id = {game_id}"

    # logger.debug(gp_version)
    # logger.debug(as_version)

    # 先处理GP
    if gp_packageName == None or gp_packageName == "":
        # logger.debug("没有谷歌包：{0}".format(name))
        pass
    else:
        version_sql1 = f"SELECT game_id, info, version FROM gp_versions WHERE game_id = {game_id} ORDER BY id DESC LIMIT 1;"
        versions1 = select_data(version_sql1)
        # logger.debug(version_sql1)
        try:
            gp_version = versions1[0]["version"]
        except Exception as e:
            gp_version = ""
            logger.error(f"{name} 数据库获取google版本失败: {e} {versions1}")
        # 直接使用接口
        gp_live = app_google(gp_packageName)
        # logger.debug(f"gp_info: {json.dumps(gp_live)}")
        try:
            live_version = gp_live["version"]
        except Exception as e:
            logger.error(f"{name} 获取gp version 失败: {e}")
            return

        if gp_version != live_version:
            logger.info(f"{name} gp发现新版本 {live_version}, 旧版本： {gp_version}")
            info = json.dumps(gp_live)
            save_sql = f"""INSERT INTO gp_versions ("game_id", "info", "version") VALUES ({game_id}, '{info.replace("'",
                                                                                                                    "''")}', '{live_version}');"""
            save_data(save_sql)
            # 获取差异
            sql_json = versions1[0]["info"]
            diff = json_tools.diff(gp_live, sql_json)
            msg = msg + f"【{name}】 有更新 from GooglePlay\n版本:{live_version}||{gp_version}\n"
            msg = msg + f"差异： {json.dumps(diff)}"
            # msg = msg + diff_msg
            # # await save_data(gp_sql)
            # logger.debug(msg)
        else:
            info = json.dumps(gp_live)
            update_sql = f"""UPDATE gp_versions SET info = '{info.replace("'",
                                                                          "''")}' where game_id = {game_id} AND version = '{gp_version}';"""
            save_data(update_sql)

    # 处理iOS
    if as_id == None or as_id == "":
        # logger.debug("没有iOS包：{0}".format(name))
        pass
    else:
        version_sql2 = f"SELECT game_id,version FROM as_version AS A WHERE NOT EXISTS (SELECT 1 FROM as_version AS b WHERE b.game_id = A.game_id AND b.id > A.id ) and game_id = {game_id}"
        versions2 = select_data(version_sql2)
        try:
            as_version = versions2[0]["version"]
        except Exception as e:
            logger.error(f"{name} 数据库获取iOS版本失败: {e}")
            as_version = ""
        try:
            as_live = app_apple(country=apple_country, id=as_id)
            live_version = as_live["version"]
            # logger.debug(name + ":" + live_version)

            if as_version == None or as_version == "":
                logger.debug("没有存:" + name)
                # as_version = "0.0"

            # 写入
            if as_version != live_version:
                logger.info(f"{name} iOS发现新版本： {live_version} | {as_version}")
                timestamp = str(int(time.time()))
                # version_info = filter_values(json.dumps(as_live["version_info"]).replace("'", "&#39;").replace("\\xa0", " "))
                as_sql = """
                    INSERT INTO as_version("game_id", "name", "age", "recent_update", "version", "rate", "version_info", "apple_url", "as_id", "timestamp", "icon", "rank")
VALUES
({0}, '{1}', '{2}', '{3}', '{4}', {5}, '{6}', '{7}', {8}, {9}, '{10}', '{11}');""" \
                    .format(game_id,
                            str(as_live["name"].replace("\'",
                                                        "\"")),
                            as_live["age"],
                            as_live["recent_update"],
                            as_live["version"],
                            as_live["rate"],
                            as_live["version_info"],
                            as_live["apple_url"],
                            as_live["as_id"],
                            timestamp,
                            as_live["icon"], as_live["rank"])
                # logger.debug(as_sql)
                # 获取差别
                # logger.debug(json.dumps(as_live))
                # diff_msg = ""
                # diff_sql = f'SELECT * FROM as_version WHERE game_id = {game_id} ORDER BY "version" DESC limit 1'
                # sql_result = select_data(diff_sql)
                # logger.debug(sql_result)
                # if sql_result != []:
                #     sql_json = dict(sql_result[0])
                #     logger.debug(sql_json)
                #     logger.debug(as_live)
                #     diff = json_tools.diff(as_live, sql_json)
                #     logger.error(json.dumps(diff))
                # else:
                #     diff = "新增游戏"

                save_data(as_sql)
                msg = msg + f"【{name}】 有更新 from AppStore\n {live_version} | {as_version} \n {as_live['apple_url']}"
                # msg += str(diff)

            else:
                update_time = int(time.time())
                update_sql = f"""UPDATE as_version SET rank = '{as_live[
                    "rank"]}', timestamp = {update_time} where game_id = {game_id} and version = '{live_version}'"""
                save_data(update_sql)
        except Exception as e:
            logger.error("app store获取版本信息失败：{0}\n{1}".format(name, str(e)))
    logger.debug(f"{name} 耗时 {timer() - time1} s")
    return msg


async def run():
    # 获取所有game_id
    app_sql = "SELECT * FROM game_info WHERE is_pulish is True order by game_id"
    result = select_data(app_sql)
    game_ids = [x["game_id"] for x in result]
    # tasks = [check_project(game_id) for game_id in game_ids]
    res = pool.map(check_project, game_ids)
    logger.debug(res)
    # msg = ""
    # for i in res:
    #     if i != "":
    #         msg += msg
    return res


if __name__ == '__main__':
    pk = "slots.machine.winning.android"
    app_id = "1546338773"
    country = "cn"
    app_id1 = "1330550298"
    country1 = ""
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(app_google(pk))
    # loop.run_until_complete(app_apple(country, app_id))

    # app_apple(country, app_id)
    check_project(101)
    # app_google(pk)

    # loop.run_until_complete(run())
    # loop.close()
