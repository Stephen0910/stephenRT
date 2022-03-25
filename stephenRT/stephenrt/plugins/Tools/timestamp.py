#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/2/28 9:44
# @Author   : StephenZ
# @Site     : 
# @File     : timestamp.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import time, re, datetime
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg
from nonebot.permission import SUPERUSER


timeStamp = on_command("time", rule=to_me(), aliases={"ts", "时间戳"}, priority=1, permission=SUPERUSER)


@timeStamp.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg("orinTime", args)  # 如果用户发送了参数则直接赋值


@timeStamp.got("orinTime", prompt="输入时间戳或者now")
async def handleuser(
        orinTime: Message = Arg()
):
    if str(orinTime) == "now":
        sTime = int(time.time())
        # mTime = int(round(sTime * 1000))
        await timeStamp.finish("当前时间戳：\n{0}".format(sTime))
    elif re.match("\d+$", str(orinTime)):
        query_time = int(str(orinTime))
        try:
            nature = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(query_time))
        except Exception as e:
            nature = "内部错误：" + str(e)
        await timeStamp.finish(nature)

    else:
        await timeStamp.finish("输入错误，查询结束")