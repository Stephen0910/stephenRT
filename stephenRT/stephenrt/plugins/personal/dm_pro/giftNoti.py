#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/5/20 10:16
# @Author   : StephenZ
# @Site     : 
# @File     : giftNoti.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import time, re, requests, json
import asyncio, time
import stephenrt.privateCfg as cfg
import websockets
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText

from nonebot.permission import SUPERUSER
from nonebot import get_bot
from nonebot import on_metaevent
import socket
import psycopg2

config = cfg.config_content
group_id = config["group_id_badminton"]
user_id = config["user_id"]
pgsql = config

first_time = int(time.time())
init_time = [first_time]
limit_money = 49

mattcher = on_metaevent()


async def get_presents(sql):
    with psycopg2.connect(user=pgsql["user"], password=pgsql["password"], database=pgsql["database"],
                          host=pgsql["host"]) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()
        return results


@mattcher.handle()
async def gift_push():
    bot = get_bot()
    sql = "SELECT nn, room_user, num, gfn, price, timestamp FROM dm where single_price > {0} and timestamp > {1} ORDER BY timestamp DESC".format(limit_money, init_time[-1])
    gifts = await get_presents(sql=sql)
    if gifts:
        init_time.append(gifts[0][-1])
        msg = ""
        for gift in gifts:
            msg += "{0} 送给 {1} {2}个 {3} ￥{4} \n".format(gift[0], gift[1], gift[2], gift[3], gift[4])
        print(msg)
        await bot.send_private_msg(user_id=user_id, message=msg)
