#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/8/12 9:14
# @Author   : StephenZ
# @Site     : 
# @File     : query_game.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import re, datetime
import requests, socket
import json
import time
from nonebot import get_bot
from nonebot import on_metaevent
from nonebot.adapters.onebot.v11.message import MessageSegment
import logzero, logging
from logzero import logger

from .shop_info import *

logzero.loglevel(logging.DEBUG)
# logzero.logfile("../../logfile.log")


game = on_metaevent()
trigger = 1


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


@game.handle()
async def query_game():
    global trigger
    # 查询的项目信息
    logger.debug("game trigger:{0}".format(trigger))
    if trigger % 30 == 0:
        # 数据库里面配置到有信息就证明有包，没有存就写入，存了就比较
        app_sql = "SELECT * FROM game_info WHERE is_pulish is True"
        app_infos = await select_data(app_sql)
        for app_info in app_infos:
            game_id = app_info["game_id"]
            gp_package, as_id, country = app_info["gp_packageName"], app_info["as_id"], app_info["apple_country"]
            if gp_package != None:  # 在gp有包
                logger.debug(game_id)
                google_info = await select_data("SELECT * FROM gp_version WHERE game_id = {0}".format(game_id))
                if google_info == []:  # 没有google版本信息，写入
                    gp_info = await gpInfo(gp_package)
                    sql = """
                    INSERT INTO gp_version ( "game_id", "name", "age", "recent_update", "version", "rate", "google_url", "gp_packageName", "sdk_min", sdk_max )
VALUES 
({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', {8}, {9});""".format(game_id, gp_info["name"],
                                                                            gp_info["age"],
                                                                            gp_info["recent_update"],
                                                                            gp_info["version"], gp_info["rate"],
                                                                            gp_info["google_url"],
                                                                            gp_info["gp_packageName"],
                                                                            gp_info["sdk_min"],
                                                                            gp_info["sdk_max"])
                    await save_data(sql)
                else:
                    gp_info = await gpInfo(gp_package)
                    last_version = max([float(x["version"]) for x in google_info])
                    logger.error(gp_info["name"].encode("utf-8"))
                    logger.error(gp_info["version"])
                    logger.error(last_version)
                    logger.error(gp_info["google_url"])
                    if version_max(gp_info["version"], last_version):
                        logger.error("新版本更新，需要写入")
                        sql = """
                        INSERT INTO gp_version ( "game_id", "name", "age", "recent_update", "version", "rate", "google_url", "gp_packageName", "sdk_min", sdk_max )
VALUES	
({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', {8}, {9});""".format(game_id, gp_info["name"],
                                                                            gp_info["age"],
                                                                            gp_info["recent_update"],
                                                                            gp_info["version"],
                                                                            gp_info["rate"],
                                                                            gp_info["google_url"],
                                                                            gp_info["gp_packageName"],
                                                                            gp_info["sdk_min"],
                                                                            gp_info["sdk_max"])

                        await save_data(sql)


                    else:
                        logger.debug("版本无变化")

            if as_id != None:  # 在iOS有包
                apple_info = await select_data("SELECT * FROM as_version WHERE as_id = {0}".format(as_id))
                if apple_info == []:  # 没有appstore 信息
                    as_info = await asInfo(country, as_id)
                    logger.debug(json.dumps(as_info))
                    rate = float(as_info["rate"])
                    logger.error(rate)
                    sql = """
                    INSERT
                    INTO
                    as_version("game_id", "name", "age", "recent_update", "version", "rate", "version_info",
                               "apple_url", "as_id")


VALUES({0}, '{1}', '{2}', '{3}', '{4}', {5}, '{6}', '{7}', {8});
""".format(game_id, str(as_info["name"]),
           as_info["age"],
           as_info["recent_update"],
           as_info["version"],
           rate, json.dumps(as_info["version_info"]),
           as_info["apple_url"], as_info["as_id"])
                    logger.debug(sql)
                    await save_data(sql)

    trigger += 1
