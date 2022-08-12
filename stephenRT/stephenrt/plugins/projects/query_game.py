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
trigger = 0


@game.handle()
async def query_game():
    global trigger
    # 查询的项目信息


    if trigger % 3 == 0:
        app_sql = "SELECT * FROM game_info WHERE is_pulish is True"
        app_info = await select_data(app_sql)
        logger.info(app_info)
