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
from .novaMS import *

logzero.loglevel(logging.DEBUG)

if __name__ == '__main__':
    from local_config import *
else:
    from .local_config import *

command = on_command("matchNova", rule=to_me(), aliases={"Debug"}, priority=1)
split_symbol = "⬤"
promot = ("机器人功能(请@我)\n输入：序号 userId\n" + "{0}  1、新账号\n" +
          "{0}  2、变强套装（满级英雄、宝石、货币）\n" + "{0}  3、切换指定账号 旧帐号 新账号\n" + "{0}  4、执行sql-progress\n" + "{0} test 执行接口测试-无参数\n").format(
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


async def add_resource(user_id, items):
    import requests
    import json
    host = pgsql["novaHost"]
    url = f"http://{host}:26601/dev/ManageAddResource"
    payload = json.dumps({
        "userId": user_id,
        "items": items
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response.close()


async def get_report(s, reportId):
    endTime = None
    report = reportDb(s, reportId)
    execute = "0"
    # while endTime == None:  # 从endTime判定
    while float(str(execute)) < 1.00:
        report = reportDb(s, reportId)
        # logger.denig(str(report))
        endTime = report["endTime"]
        execute = str(report["executeRate"])
        time.sleep(2)
    else:
        errorStep = 0

    for i in report["apiScenarioStepData"]:
        if i["status"] == "PENDING":
            pendingStep = i["count"]
            break
    else:
        pendingStep = 0

    for i in report["apiScenarioStepData"]:
        if i["status"] == "ERROR":
            errorStep = i["count"]
            break
    else:
        errorStep = 0

    allStep = sum([int(x["count"]) for x in report["apiScenarioStepData"]])
    stepRate = (allStep - int(errorStep) - int(pendingStep)) / allStep
    stepRate = "{:.2%}".format(stepRate)
    report["步骤通过率"] = f"{stepRate} [{allStep - int(errorStep) - int(pendingStep)} / {allStep}]"

    msg = "【API TEST complete】:\n"
    apis = get_interfaceList(s, report["interfaceReport"])
    apiCover = api_cover(s, 200, projectId)
    # apiNot = list(set(apis) ^ set(apiCover))
    apiNot = []
    for i in apis:
        if i not in apiCover:
            apiNot.append(i)
    coverLen = len(apis) - len(apiNot)
    apiRate = "{:.2%}".format(coverLen / len(apis))
    report["接口覆盖率"] = f"{apiRate} [{str(coverLen)}/{str(len(apis))}]"
    report["未覆盖接口"] = str(apiNot)
    keyword = ["测试计划", "耗时", "接口覆盖率", "场景通过率", "步骤通过率", "失败场景", "未覆盖接口"]
    cost = (report['endTime'] - report['startTime']) / 1000
    report["耗时"] = f"{cost} s"

    for key in keyword:
        msg = msg + str(key) + "：" + str(report[key]) + "\n"
    return msg


async def deal_command(userInput):
    inputList = userInput.split(" ")
    try:
        op, user_id = str(inputList[0]), int(inputList[1])
    except:
        return "输入参数错误, 结束会话"
    message = "执行成功"
    if op == "1":
        if len(inputList) != 2:
            return "输入错误， 请按照正确格式输入"
        sqls = [
            f"DELETE from account_bind_info WHERE unique_id in (SELECT email_name FROM account_bind_info WHERE user_id = {user_id});",
            f"DELETE from device_info WHERE user_id = {user_id};"]
        await exeSql(sqls)

    elif op == "2":
        if len(inputList) != 2:
            return "输入错误， 请按照正确格式输入"
        items = [
            {
                "type": 7,
                "num": 4,
                "id": 10
            },
            {
                "type": 8,
                "num": 4,
                "id": 110
            },
            {
                "type": 8,
                "num": 4,
                "id": 210
            },
            {
                "type": 8,
                "num": 4,
                "id": 310
            },
            {
                "type": 8,
                "num": 4,
                "id": 410
            },
            {
                "type": 9,
                "num": 1,
                "id": 105
            },
            {
                "type": 9,
                "num": 1,
                "id": 205
            },
            {
                "type": 9,
                "num": 1,
                "id": 305
            },
            {
                "type": 9,
                "num": 1,
                "id": 405
            },
            {
                "type": 10,
                "num": 2,
                "id": 105
            },
            {
                "type": 10,
                "num": 2,
                "id": 205
            },
            {
                "type": 10,
                "num": 2,
                "id": 305
            },
            {
                "type": 10,
                "num": 2,
                "id": 405
            }
        ]
        await add_resource(user_id, items)

        await exeSql(
            [f"update user_info set ut = ut + 100000, gt = gt + 1, bnb = bnb + 10000 where user_id = {user_id}",
             f"UPDATE hero_info SET level = 25, usable_points = 200 WHERE id in (SELECT id from hero_info where user_id = {user_id} and status = 1 ORDER BY id DESC LIMIT 4);"], )
        # messsage = "执行成功"

    elif op == "3":
        try:
            userOld, userNew = int(inputList[1]), int(inputList[2])
            sql = f"""
                    UPDATE account_bind_info ac set user_id = (
            	case when ac.user_id = {userOld} then {userNew} 
              when ac.user_id = {userNew} then {userOld} end
            ) where ac.user_id in ({userOld},{userNew}) returning id, user_id;
                    """
        except:
            return "输入参数错误, 结束会话"

        await exeSql([sql])
        return "执行成功"
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
    userInput = str(userInput)
    print("userInput:", userInput)
    if userInput == "test":
        result = exec_run(access_key, secret_key, host, projectId, envId, testPlan_id)
        reportId, msg = result
        await command.send(msg)
        setHeaders(s, access_key, secret_key)
        try:
            reportMsg = await get_report(s, reportId)
        except Exception as e:
            reportMsg = f"内部错误,结束会话： {str(e)}"
        await command.finish(reportMsg)

    response = await deal_command(userInput)
    await command.finish(response)
