#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/2/24 15:44
# @Author   : StephenZ
# @Site     : 
# @File     : helpFile.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

from nonebot import require, get_bot, get_driver
import nonebot
# from .report import *
import datetime, time, re
from nonebot.adapters.onebot.v11.message import MessageSegment

from nonebot import on_command
from nonebot.rule import to_me
from nonebot.params import ArgPlainText

from nonebot.permission import SUPERUSER

help = on_command("help", rule=to_me(), aliases={"帮助", "菜单", "使用"}, priority=1)

split_symbol = "⬤"
msg = (
        "机器人功能(请@我 并加/命令呼出 需添加权限)：\n" + "{0}  zendesk工单统计(/zen /zendesk /工单)\n" +
        "{0}  Q群聊天统计+词云(/report /日报 /词云)\n" + "{0}  敏感词检测（测试中）\n" + "{0}  羽毛球查询(/find /findt为测试服)、禁言(/ban)\n").format(
    split_symbol)

tools = "{0}  时间戳 /ts".format(split_symbol)
msg += tools


@help.got("noparam", prompt=msg)
async def zendeskReport():
    await help.finish()
