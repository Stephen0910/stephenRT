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

from nonebot.plugin import require
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
import jieba
import asyncpg
from nonebot.adapters.onebot.v11 import PrivateMessageEvent, Bot
from nonebot import on_message
import time, datetime

requireA = require("chatRecord")
config = requireA.config
print("config:", config)

private_matcher = on_message()

async def getRecord(group_id, day):
    timestamp = int(time.time())
    conn = await asyncpg.connect(user=config["user"], password=config["password"], database=config["database"],
                                 host=config["host"])
    day2second = timestamp - day*86400
    day2time = datetime.datetime.fromtimestamp(day2second)
    selectSql = """SELECT message FROM "group" WHERE group_id = {0} and "timestamp" > '{1}'""".format(group_id, day2time)
    print(selectSql)
    contents = await conn.fetch(selectSql)
    await conn.close()
    return contents


@private_matcher.handle()
async def saveMsg(bot: Bot, event: PrivateMessageEvent):
    msg = event
    result =await getRecord(group_id=768887710, day=1)
    print("result:\n", result)