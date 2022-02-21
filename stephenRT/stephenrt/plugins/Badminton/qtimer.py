#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/2/18 10:56
# @Author   : StephenZ
# @Site     : 
# @File     : qtimer.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>
"""
待定
"""

from nonebot import require, get_bot
import datetime, time
from nonebot.adapters.onebot.v11.message import MessageSegment
import asyncpg
import re, os
from stephenrt.privateCfg import config_content

scheduler = require("nonebot_plugin_apscheduler").scheduler
config = config_content
keywords = ["吗", "难道", "怎么", "呢", "么"]


async def getRecord(group_id, timestamp):
    conn = await asyncpg.connect(user=config["user"], password=config["password"], database=config["database"],
                                 host=config["host"])
    if re.match("\d+\d", str(group_id)):
        print("输入的类型是数字")
        sql = """SELECT message, sender_id, sender_name, group_card FROM "group" WHERE "group_id" = {0} and "timestamp" > '{1}'""".format(
            group_id, timestamp)
    else:
        print("输入的类型是字符")
        sql = """SELECT message, sender_id, sender_name, group_card FROM "group" WHERE "upper"(group_name) like "upper"('%{0}%') and "timestamp" > '{1}'""".format(
            group_id, timestamp)
    print("recordSql:", sql)
    msgs = await conn.fetch(sql)
    await conn.close()
    return msgs


def questsions():
    pass


@scheduler.scheduled_job("cron", hour=11, minute=11, second=0)
async def send_message():
    bot = get_bot()
    day = 1
    dateArray = datetime.datetime.utcfromtimestamp(time.time() - 86400 * day + 8 * 3600)  # 时区加8)
    checkTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
    msgs = await getRecord("羽毛球", checkTime)
    print("msgs:", msgs)
