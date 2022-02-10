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
from nonebot import on_message, on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
import time, datetime, sys

# import stephenRT.stephenrt.privateCfg as cfg
sys.path.append("../../")
import stephenrt.privateCfg as cfg
import stephenrt.report as report

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

@dailyReport.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/日报 上海，则args为上海
    if plain_text:
        matcher.set_arg("day", args)  # 如果用户发送了参数则直接赋值
        await dailyReport.send(plain_text)
