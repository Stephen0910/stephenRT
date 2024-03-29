#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/1/30 21:42
# @Author   : StephenZ
# @Site     : 
# @File     : __init__.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

# from nonebot.plugin import require
import asyncpg
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
import time, datetime, sys, datetime
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot.params import ArgPlainText
from nonebot.permission import SUPERUSER

# import stephenRT.stephenrt.privateCfg as cfg
sys.path.append("../../")
import stephenrt.privateCfg as cfg
from .report import *
from .timer import group_name, deleteFile

# from stephenrt.plugins.chatCloud import timer

config = cfg.config_content


async def getGroup(key):
    conn = await asyncpg.connect(user=config["user"], password=config["password"], database=config["database"],
                                 host=config["host"])
    selectSql = """SELECT DISTINCT group_id, group_name FROM "group" WHERE "upper"(group_name) like "upper"('%{0}%') ORDER BY group_name;""".format(
        key)
    print(selectSql)
    contents = await conn.fetchall(selectSql)
    await conn.close()
    return contents


# 以下为命令触发
dailyReport = on_command("report", rule=to_me(), aliases={"日报", "词云", "查询"}, priority=1, permission=SUPERUSER)


@dailyReport.got("groupId", prompt="请输入群号或关键词")
@dailyReport.got("days", prompt="请输入天数")
async def dailyReportHandle(
        groupId: str = ArgPlainText("groupId"),
        days: str = ArgPlainText("days"),
):
    if re.match("\d+|\d+.\d", days):
        if 0 <= float(days) <= 100:
            selectDays = float(days)
            dateArray = datetime.datetime.utcfromtimestamp(time.time() - int(86400 * selectDays) + 8 * 3600)  # 时区加8)
            msg_time = dateArray.strftime("%Y-%m-%d %H:%M:%S")
            # 获取群名
            if re.match("\d+\d", groupId):
                groupName = await group_name(groupId)
                group_info = " " * 5 + "{0}({1})\n".format(groupName, groupId)
            else:
                groups = await getGroup(groupId)
                groups_str = ""
                for group in groups:
                    groups_str = groups_str + group["group_name"] + str(group["group_id"])

                group_info = "({0})相关：".format(groupId) + groups_str + "\n"

            messages = report.Report().createPic(group_id=groupId, timestamp=msg_time)
            print("messages:", messages[1])
            await dailyReport.send(group_info + messages[0])
            await dailyReport.send(message=MessageSegment.image(file="file:///" + messages[1]))
            deleteFile(messages[1])
            await dailyReport.finish()
        else:
            await dailyReport.finish("天数过大，查询结束")  # type: ignore
    else:
        await dailyReport.finish("输入错误，重新开始")  # type: ignore
