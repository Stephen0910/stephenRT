#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/3/3 7:47
# @Author   : StephenZ
# @Site     : 
# @File     : mNova.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2023
# @Licence  :     <@2022>

import time, re, datetime
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg
from nonebot.permission import SUPERUSER
import psycopg2
import logzero, logging
from logzero import logger
from psycopg2.extras import RealDictCursor

logzero.loglevel(logging.DEBUG)

if __name__ == '__main__':
    from local_config import *
else:
    from .local_config import *




command = on_command("matchNova", rule=to_me(), aliases={"Debug"}, priority=1, permission=SUPERUSER)
split_symbol = "⬤"
promot = (
        "机器人功能(请@我 输入指定序号功能 userId)：\n" + "{0}  1、新账号\n" +
        "{0}2、 变强套装（满级英雄、宝石、货币10000）\n" + "{0}  3、货币切换\n" + "{0}待定\n").format(
    split_symbol)


async def exeSql(sql):
    with psycopg2.connect(user=pgsql["novaUser"], password=pgsql["novaPassword"], database=pgsql["novaDatabase"],
                          host=pgsql["novaHost"]) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                logger.error("sql执行失败：\n{0}\n{1}".format(str(e), sql))

@command.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数
    if plain_text:
        matcher.set_arg("orinTime", args)  # 如果用户发送了参数则直接赋值


@command.got("orinTime", prompt=promot)
async def handleuser(
        userInput: Message = Arg()
):
    try:
        userInput = userInput.split(" ")
        print("userInput:", userInput)
    except Exception as e:
        await command.finish("输入错误：" + str(e))


    # orinTime = str(orinTime)
    # print("输入为：{0}".format(orinTime))
    # if orinTime == "now":
    #     sTime = int(time.time())
    #     nature = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(sTime))
    #     # mTime = int(round(sTime * 1000))
    #     await command.finish("当前时间：{0}\n时间戳: {1}".format(nature, sTime))
    # elif re.match("^\d+$", orinTime):
    #     query_time = int(orinTime)
    #     try:
    #         if query_time > 3653284221:
    #             query_time = round(query_time / 1000)
    #         nature = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(query_time))
    #     except Exception as e:
    #         nature = "内部错误：" + str(e)
    #     await command.finish(nature)
    # else:
    #     try:
    #         input_time = re.findall("\d+", orinTime)
    #         shijian = "-".join(input_time)
    #         print(shijian)
    #         timeArray = time.strptime(shijian, "%Y-%m-%d-%H-%M-%S")
    #
    #         # 转换为时间戳:
    #
    #         nature = int(time.mktime(timeArray))
    #
    #         await command.finish(str(nature))
    #     except Exception as e:
    #         if str(e) != "":
    #             await command.finish(str(e))
    #     finally:
    #         pass
