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

# import stephenRT.stephenrt.privateCfg as cfg
sys.path.append("../../")
import stephenrt.privateCfg as cfg
from .report import *
from .timer import group_name

from stephenrt.plugins.chatCloud import timer

config = cfg.config_content

async def getRecord(group_id, day):
    timestamp = int(time.time())
    conn = await asyncpg.connect(user=config["user"], password=config["password"], database=config["database"],
                                 host=config["host"])
    day2second = timestamp - day * 86400
    day2time = datetime.datetime.fromtimestamp(day2second)
    selectSql = """SELECT message FROM "group" WHERE group_id = {0} and "timestamp" > '{1}'""".format(group_id,
                                                                                                      day2time)
    print("selectSql:", selectSql)
    contents = await conn.fetch(selectSql)
    await conn.close()
    return contents


# @private_matcher.handle()
# async def saveMsg(bot: Bot, event: PrivateMessageEvent):
#     msg = event
#     result = await getRecord(group_id=768887710, day=1)
#     print("result:\n", result)
#     print(len(result))

# 以下为命令触发
dailyReport = on_command("report", rule=to_me(), aliases={"日报", "词云"}, priority=1)


# @dailyReport.handle()
# async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
#     plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/日报 上海，则args为上海
#     # test = "file:///D:\Code\inside\stephenRT\stephenRT\stephenrt\pictures\wordcloud_645286417.png".replace("\\", "/")
#     if plain_text:
#         day = 1
#         dateArray = datetime.datetime.utcfromtimestamp(time.time() - 86400 * day + 8 * 3600)  # 时区加8)
#         msg_time = dateArray.strftime("%Y-%m-%d %H:%M:%S")
#         checkTime = msg_time
#         print("checktime:", checkTime)
#         matcher.set_arg("group_id", args)  # 如果用户发送了参数则直接赋值
#         # await dailyReport.send(report_msg)
#         messages = report.Report().createPic(group_id=args, timestamp=checkTime)
#         print("message::::::::", messages)
#         await dailyReport.send(messages[0])
#         await dailyReport.finish(message=MessageSegment.image(file=messages[1]))



@dailyReport.got("groupId", prompt="请输入群号")
@dailyReport.got("days", prompt="请输入天数")
async def dailyReportHandle(
        groupId: str = ArgPlainText("groupId"),
        days: str = ArgPlainText("days"),
):
    if days.isdigit():
        if 1 <= int(days) <= 10:
            font_size = int(days)
            dateArray = datetime.datetime.utcfromtimestamp(time.time() - 86400 * font_size + 8 * 3600)  # 时区加8)
            msg_time = dateArray.strftime("%Y-%m-%d %H:%M:%S")
            # 获取群名
            groupName = await group_name(groupId)
            group_info = " " * 5 + "{0}({1})\n".format(groupName, groupId)
            messages = report.Report().createPic(group_id=groupId, timestamp=msg_time)
            await dailyReport.send(group_info + messages[0])
            await dailyReport.finish(message=MessageSegment.image(file=messages[1]))
        else:
            await dailyReport.finish("天数过大，查询结束")  # type: ignore
    else:
        await dailyReport.finish("输入错误，重新开始")  # type: ignore
