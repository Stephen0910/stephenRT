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
import socket
import json
import time
from nonebot import get_bot
from nonebot import on_metaevent
from nonebot.adapters.onebot.v11.message import MessageSegment
import logzero, logging
from logzero import logger
from .live_info import *

from .shop_info import *

# logzero.logfile("../../logfile.log")


game = on_metaevent()
trigger = 1


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


ip = str(get_host_ip())

if re.match("192.*", ip):
    # from .dGame import *
    # from .dm_pro.live import *
    # from .search_body import *
    # from .nba.season import *
    # from .kuake import *
    # from .wPublic import *
    group = 755489024
    pass

if ip == "10.10.10.8":
    print("本地内网")

if ip == "172.24.121.72":
    group = 755489024
    pass


@game.handle()
async def query_game():
    global trigger
    bot = get_bot()
    # 查询的项目信息
    logger.debug("project trigger:{0}".format(trigger))
    #     if trigger % 3 == 0:
    #         # 数据库里面配置到有信息就证明有包，没有存就写入，存了就比较
    #         app_sql = "SELECT * FROM game_info WHERE is_pulish is True"
    #         app_infos = await select_data(app_sql)
    #         logger.info("infos-------------:", app_infos)
    #         for app_info in app_infos:
    #             logger.info("SQL:", app_info["name"])
    #             game_id = app_info["game_id"]
    #             gp_package, as_id, country = app_info["gp_packageName"], app_info["as_id"], app_info["apple_country"]
    #             if gp_package != None and gp_package != "":  # 在gp有包
    #                 google_info = await select_data(
    #                     "SELECT * FROM gp_version WHERE game_id = {0} ORDER BY id DESC".format(game_id))
    #                 if google_info == []:  # 没有google版本信息，写入
    #                     logger.info("没有google版本信息，写入：{0}".format(app_info["name"]))
    #                     try:
    #                         gp_info = await gpInfo(gp_package)
    #                     except:
    #                         logger.error("获取GP信息错误:{0}".format(gp_package))
    #                         break
    #                     sql = """
    #                     INSERT INTO gp_version ( "game_id", "name", "age", "recent_update", "version", "rate", "google_url", "gp_packageName", "sdk_min", sdk_max )
    # VALUES
    # ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', {8}, {9});""".format(game_id,
    #                                                                             gp_info["name"].replace("\'", "\""),
    #                                                                             gp_info["age"],
    #                                                                             gp_info["recent_update"],
    #                                                                             gp_info["version"], gp_info["rate"],
    #                                                                             gp_info["google_url"],
    #                                                                             gp_info["gp_packageName"],
    #                                                                             gp_info["sdk_min"],
    #                                                                             gp_info["sdk_max"])
    #                     await save_data(sql)
    #                 else:
    #                     gp_info = await gpInfo(gp_package)
    #                     # last_version = max([float(x["version"]) for x in google_info])  # 三位出错
    #                     last_version = google_info[0]["version"]
    #                     is_upgrade = await version_max(gp_info["version"], last_version)
    #                     if is_upgrade:
    #                         logger.info("新版本更新，需要写入")
    #                         sql = """
    #                         INSERT INTO gp_version ( "game_id", "name", "age", "recent_update", "version", "rate", "google_url", "gp_packageName", "sdk_min", sdk_max )
    # VALUES
    # ({0}, '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', {8}, {9});""".format(game_id,
    #                                                                             gp_info["name"].replace("\'", "\""),
    #                                                                             gp_info["age"],
    #                                                                             gp_info["recent_update"],
    #                                                                             gp_info["version"],
    #                                                                             gp_info["rate"],
    #                                                                             gp_info["google_url"],
    #                                                                             gp_info["gp_packageName"],
    #                                                                             gp_info["sdk_min"],
    #                                                                             gp_info["sdk_max"])
    #
    #                         msg = "【{0}】 有更新 from GooglePlay\n版本:{1}||{3}\n{2}".format(gp_info["name"], gp_info["version"],
    #                                                                                    gp_info["google_url"], last_version)
    #                         await save_data(sql)
    #                         try:
    #                             await bot.send_group_msg(group_id=group, message=msg)
    #                         except Exception as e:
    #                             await bot.send_private_msg(user_id=281016636, message=msg + str(e))
    #                         finally:
    #                             return
    #
    #
    #                     else:
    #                         print("GP版本无变化:{0} {1}".format(gp_info["name"], gp_info["version"]))
    #
    #             """
    #             iOS 处理-----------------------------------------------------------------------------------------------
    #             """
    #             if as_id != None:  # 在iOS有包
    #                 apple_info_sql = await select_data(
    #                     "SELECT * FROM as_version WHERE as_id = {0} ORDER BY id DESC".format(as_id))
    #                 if apple_info_sql == []:  # 没有appStore 信息
    #                     logger.info("没有appStore 信息，写入:{0}".format(apple_info_sql["name"]))
    #                     try:
    #                         as_info_store = await asInfo(country, as_id)  # 从商店获取的
    #                     except:
    #                         logger.error("从appstore商店获取失败:{0} + {1}".format(country, as_id))
    #                         return
    #                     # logger.debug(json.dumps(as_info))
    #                     rate = float(as_info_store["rate"])
    #                     sql = """
    #                     INSERT INTO
    # as_version("game_id", "name", "age", "recent_update", "version", "rate", "version_info", "apple_url", "as_id")
    # VALUES
    # ({0}, '{1}', '{2}', '{3}', '{4}', {5}, '{6}', '{7}', {8});
    # """.format(game_id, str(as_info_store["name"].replace("\'", "\"")),
    #            as_info_store["age"],
    #            as_info_store["recent_update"],
    #            as_info_store["version"],
    #            rate, json.dumps(as_info_store["version_info"]).replace("\'", "\""),
    #            as_info_store["apple_url"], as_info_store["as_id"])
    #                     await save_data(sql)
    #
    #                 else:
    #                     try:
    #                         as_info_store = await asInfo(country, as_id)
    #                     except:
    #                         logger.error("从appstore商店获取失败:{0}".format(country, as_id))
    #                         return
    #                     last_version = apple_info_sql[0]["version"]
    #                     is_upgrade = await version_max(as_info_store["version"], last_version)
    #                     if is_upgrade:
    #                         logger.info("新版本更新，需要写入")
    #                         sql = """
    #                                             INSERT INTO
    #                         as_version("game_id", "name", "age", "recent_update", "version", "rate", "version_info", "apple_url", "as_id")
    #                         VALUES
    #                         ({0}, '{1}', '{2}', '{3}', '{4}', {5}, '{6}', '{7}', {8});
    #                         """.format(game_id, str(as_info_store["name"].replace("\'", "\"")),
    #                                    as_info_store["age"],
    #                                    as_info_store["recent_update"],
    #                                    as_info_store["version"],
    #                                    as_info_store["rate"], json.dumps(as_info_store["version_info"]).replace("\'", "\""),
    #                                    as_info_store["apple_url"], as_info_store["as_id"])
    #                         await save_data(sql)
    #
    #                         msg = "【{0}】 有更新 from AppStore\n版本:{1}||{3}\n{2}".format(str(as_info_store["name"]),
    #                                                                                 as_info_store["version"],
    #                                                                                 as_info_store["apple_url"],
    #                                                                                 last_version)
    #                         await save_data(sql)
    #                         try:
    #                             await bot.send_group_msg(group_id=group, message=msg)
    #                         except Exception as e:
    #                             await bot.send_private_msg(user_id=281016636, message=msg + str(e))
    #                         finally:
    #                             return
    #
    #                     else:
    #                         print("AS版本无变化{0}: {1}".format(as_info_store["name"], as_info_store["version"]))
    #
    #         logger.info("执行完成一轮查询")

    if trigger % 20 == 0:
        trigger += 1  # 有可能执行得满了，超过了5s，第二次轮询进来trigger还没加，所以在这里先加1 避免重复执行
        respon = await run()
        logger.info(respon)
        msg = "".join([x for x in list(set(respon)) if x != ""])
        if msg != "":
            print("msg++\n", msg)
            try:
                await bot.send_private_msg(user_id=281016636, message=msg)
            except Exception as e:
                logger.error(str(e))
                await bot.send_private_msg(user_id=281016636, message=str(e))
    trigger += 1
