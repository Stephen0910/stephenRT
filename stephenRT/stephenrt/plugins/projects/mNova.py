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
import requests, json

logzero.loglevel(logging.DEBUG)

if __name__ == '__main__':
    from local_config import *
else:
    from .local_config import *

command = on_command("matchNova", rule=to_me(), aliases={"Debug"}, priority=1, permission=SUPERUSER)
split_symbol = "⬤"
promot = ("机器人功能(请@我\n输入：序号 userId)：\n" + "{0}  1、新账号\n" +
          "{0}  2、变强套装（满级英雄、宝石、货币10000）\n" + "{0}  3、货币切换\n" + "{0}  待定\n").format(
    split_symbol)


async def exeSql(sqls):
    with psycopg2.connect(user=pgsql["user"], password=pgsql["novaPassword"], database=pgsql["novaDatabase"],
                          host=pgsql["novaHost"]) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            try:
                [cursor.execute(sql) for sql in sqls]
                # cursor.execute(sql)
                conn.commit()
            except Exception as e:
                logger.error("sql执行失败：\n{0}".format(str(e)))


async def add_resource(user_id, type, num, id):
    import requests
    import json
    host = pgsql["novaHost"]
    url = f"http://{host}:26601/dev/ManageAddResource"
    payload = json.dumps({
        "userId": user_id,
        "items": [
            {
                "type": type,
                "num": num,
                "id": id
            }
        ]
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response.close()


async def deal_command(userInput):
    inputList = userInput.split(" ")
    op, user_id = str(inputList[0]), int(inputList[1])
    if op == "1":
        sqls = [
            f"DELETE from account_bind_info WHERE unique_id in (SELECT email_name FROM account_bind_info WHERE user_id = {user_id});",
            f"DELETE from device_info WHERE user_id = {user_id};"]
        await exeSql(sqls)
        message = "执行成功"
    elif op == "2":
        await add_resource(user_id, 7, 4, 10)
        await add_resource(user_id, 8, 3, 110)
        await add_resource(user_id, 8, 3, 210)
        await add_resource(user_id, 8, 3, 310)
        await add_resource(user_id, 8, 3, 410)
        await add_resource(user_id, 9, 1, 105)
        await add_resource(user_id, 9, 1, 205)
        await add_resource(user_id, 9, 1, 305)
        await add_resource(user_id, 9, 1, 405)
        await exeSql(
            [f"update user_info set ut = ut + 10000, gt = gt + 10000, bnb = bnb + 10000 where user_id = {user_id}",
             f"UPDATE hero_info SET level = 30 WHERE id in (SELECT id from hero_info where user_id = {user_id} and status = 1 ORDER BY id DESC LIMIT 4);"])
        messsage = "执行成功"

    elif op == "3":
        pass
    else:
        message = "操作方式错误"
    return message


@command.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数
    if plain_text:
        matcher.set_arg("userInput", args)  # 如果用户发送了参数则直接赋值


@command.got("userInput", prompt=promot)
async def handleuser(
        userInput: Message = Arg()
):
    try:
        userInput = str(userInput)
        print("userInput:", userInput)
        response = await deal_command(userInput)
        await command.finish(response)
    except Exception as e:
        await command.finish("执行错误：" + str(e))

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
