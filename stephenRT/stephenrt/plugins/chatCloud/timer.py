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
from stephenrt.pulgins.chatCloud.report import report
import stephenrt.privateCfg as cfg
import datetime, time
from nonebot.adapters.onebot.v11.message import MessageSegment
import asyncpg


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
    except:
        groupName = "未查询到指定群名，检查群号"
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

groups = [581529846, 135313433, 768887710, 672076603, 645286417, 790318000]


# groups = [581529846]


@scheduler.scheduled_job("cron", hour="*", minute="*", second=0)
async def send_message():
    bot = get_bot()
    for group in groups:
        day = 1
        groupName = await group_name(group)
        dateArray = datetime.datetime.utcfromtimestamp(time.time() - 86400 * day + 8 * 3600)  # 时区加8)
        checkTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
        messages = report.Report().createPic(group_id=group, timestamp=checkTime)
        group_info = " " * 5 + "{0}({1})\n".format(groupName, group)
        can_send_image = await bot.can_send_image()
        print("是否可发送图片:", can_send_image["yes"])
        await bot.send_private_msg(user_id=281016636, message=group_info + messages[0])
        await bot.send_private_msg(user_id=281016636, message=MessageSegment.image(file=messages[1]))
        time.sleep(3)

# scheduler.add_job(send_message, "interval", days=1, id="xxx")
# print("定时器触发成功")
