#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/2/12 10:09
# @Author   : StephenZ
# @Site     : 
# @File     : timer.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

from nonebot import require, get_bot
# from .report import *
from stephenrt.plugins.chatCloud import report
import stephenrt.privateCfg as cfg
import datetime, time
from nonebot.adapters.onebot.v11.message import MessageSegment
import asyncpg
import re


async def getGroup(key):
    conn = await asyncpg.connect(user=config["user"], password=config["password"], database=config["database"],
                                 host=config["host"])
    selectSql = """SELECT DISTINCT group_id, group_name FROM "group" WHERE "upper"(group_name) like "upper"('%{0}%') ORDER BY group_name;""".format(
        key)
    print(selectSql)
    contents = await conn.fetch(selectSql)
    await conn.close()
    print("grouoooooo:", contents)
    return contents


# 导入对象
scheduler = require("nonebot_plugin_apscheduler").scheduler

config = cfg.config_content


async def group_name(group_id):
    conn = await asyncpg.connect(user=config["user"], password=config["password"], database=config["database"],
                                 host=config["host"])
    selectSql = """
    SELECT group_name FROM "group" WHERE group_id = {0} LIMIT 1;
    """.format(group_id)
    try:
        name = await conn.fetchrow(selectSql)
        groupName = name["group_name"]
    except Exception as e:
        groupName = e
    await conn.close()
    return groupName


#
# @scheduler.scheduled_job("cron", hour="*", id="1")
# async def run_every_2_hour():
#     print("定时器内容？？？？？？？")
#
#
# scheduler.add_job(run_every_2_hour, "interval", days=1, id="2")
# print("定时器触发成功")

checkGroups = [768887710, 581529846, 135313433, "羽毛球"]


# nonebot,home,手游

# groups = [581529846]


@scheduler.scheduled_job("cron", hour=23, minute=0, second=0)
async def send_message():
    bot = get_bot()
    day = 1
    dateArray = datetime.datetime.utcfromtimestamp(time.time() - 86400 * day + 8 * 3600)  # 时区加8)
    checkTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
    for group in checkGroups:
        print("发送：", group)
        if re.match("\d+\d", str(group)):
            groupName = await group_name(group)

            group_info = " " * 5 + "{0}({1})\n".format(groupName, group)
            # messages = report.Report().createPic(group_id=group, timestamp=checkTime)
        else:
            groups = await getGroup(key=group)
            groups_str = ""
            for group_info in groups:
                groups_str = groups_str + group_info["group_name"] + str(group_info["group_id"])
            group_info = "({0})相关：".format(group) + groups_str + "\n"
        messages = report.Report().createPic(group_id=group, timestamp=checkTime)
        await bot.send_private_msg(user_id=281016636, message=group_info + messages[0])
        await bot.send_private_msg(user_id=281016636, message=MessageSegment.image(file=messages[1]))

# scheduler.add_job(send_message, "interval", days=1, id="xxx")
# print("定时器触发成功")
