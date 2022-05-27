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


@timeStamp.got("orinTime", prompt="输入时间(年月日时分秒)/时间戳/now")
async def handleuser(
        orinTime: Message = Arg()
):
    orinTime = str(orinTime)
    print("输入为：{0}".format(orinTime))
    if orinTime == "now":
        sTime = int(time.time())
        nature = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sTime))
        # mTime = int(round(sTime * 1000))
        await timeStamp.finish("当前时间：{0}\n时间戳: {1}".format(nature, sTime))
    elif re.match("^\d+$", orinTime):
        query_time = int(orinTime)
        try:
            if query_time > 3653284221:
                query_time = round(query_time / 1000)
            nature = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(query_time))
        except Exception as e:
            nature = "内部错误：" + str(e)
        await timeStamp.finish(nature)
    else:
        try:
            input_time = re.findall("\d+", orinTime)
            shijian = "-".join(input_time)
            print(shijian)
            timeArray = time.strptime(shijian, "%Y-%m-%d-%H-%M-%S")

            # 转换为时间戳:

            nature = int(time.mktime(timeArray))

            await timeStamp.finish(str(nature))
        except Exception as e:
            if str(e) != "":
                await timeStamp.finish(str(e))
        finally:
            pass
