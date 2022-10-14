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

    if trigger % 40 == 0:
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
