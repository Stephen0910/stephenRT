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
"""
定时器，定时发送报告-》包括发言top3 关键词top5 词云
"""

from nonebot import require, get_bot
# from .report import *
from stephenrt.plugins.chatCloud import report
import stephenrt.privateCfg as cfg
import datetime, time
from nonebot.adapters.onebot.v11.message import MessageSegment
import asyncpg
import re, os


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


def deleteFile(filepath):
    print("删除中。。。")
    time.sleep(5)
    if os.path.exists(filepath):  # 如果文件存在
        os.remove(filepath)
        print("删除成功")
    else:
        print('删除失败：no such file:%s' % filepath)  # 则返回文件不存在


# 导入对象
scheduler = require("nonebot_plugin_apscheduler").scheduler

config = cfg.config_content

user_id = config["user_id"]
group_id = config["group_id_test"]


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

# checkGroups = [768887710, 581529846, 135313433, "羽毛球"]
checkGroups = ["决战羽毛球"]


# nonebot,home,手游

# groups = [581529846]


@scheduler.scheduled_job("cron", hour=23, minute=0, second=0)
async def send_message():
    # bot = get_bot()
    # day = 1
    # dateArray = datetime.datetime.utcfromtimestamp(time.time() - 86400 * day + 8 * 3600)  # 时区加8)
    # yesArray = datetime.datetime.utcfromtimestamp(time.time() - 86400 * (day + 1) + 8 * 3600)
    # checkTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
    # yescheck = yesArray.strftime("%Y-%m-%d %H:%M:%S")
    # print(checkTime)
    # for group in checkGroups:
    #     print("发送：", group)
    #     if re.match("\d+\d", str(group)):
    #         groupName = await group_name(group)
    #
    #         group_info = " " * 5 + "{0}({1})\n".format(groupName, group)
    #         # messages = report.Report().createPic(group_id=group, timestamp=checkTime)
    #     else:
    #         groups = await getGroup(key=group)
    #         groups_str = ""
    #         for group_info in groups:
    #             groups_str = groups_str + group_info["group_name"] + str(group_info["group_id"])
    #         group_info = "({0})相关：".format(group) + groups_str + "\n"
    #     messages = report.Report().createPic(group_id=group, timestamp=checkTime)
    #     todayCount = report.Report().wordReport(group_id=group, timestamp=checkTime)[2]
    #     yesCount = report.Report().wordReport(group_id=group, timestamp=yescheck)[2] - todayCount
    #     change = "增加" if todayCount > yesCount else "减少"
    #     change_rate = '{:.2%}'.format((abs(todayCount - yesCount)) / yesCount)
    #     compare = "今天总计：{0}, 昨天总计{1}, 同比{2} {3}\n".format(todayCount, yesCount, change, change_rate)
    #     group_info += compare
    #     try:
    #         await bot.send_group_msg(group_id=group_id, message=group_info + messages[0])
    #
    #     except Exception as e:
    #         # await bot.send_private_msg(user_id=user_id, messages=str(e))
    #         await bot.send_private_msg(user_id=281016636, message=group_info + messages[0] + compare)
    #
    #     try:
    #         await bot.send_group_msg(group_id=group_id, message=MessageSegment.image(file="file:///" + messages[1]))
    #     except Exception as e:
    #         # await bot.send_private_msg(user_id=user_id, messages=str(e))
    #         await bot.send_private_msg(user_id=281016636, message=MessageSegment.image(file="file:///" + messages[1]))

        # deleteFile(messages[1])
        pass

# scheduler.add_job(send_message, "interval", days=1, id="1")
# print("定时器timer触发成功")


