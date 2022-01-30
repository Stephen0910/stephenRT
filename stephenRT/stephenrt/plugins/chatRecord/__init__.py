#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/1/29 16:14
# @Author   : StephenZ
# @Site     : 
# @File     : __init__.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2020>

from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Event
from nonebot import on_message
# from config import get_config
# import config
import asyncpg
import datetime
import json
import os


def get_config():
    """
    配置数据库信息和收取保存失败的qq号
    :return:
    """
    up_dir = os.path.abspath(os.path.join(os.getcwd(), "../../"))
    config_path = os.path.join(up_dir, "config.json")
    with open(config_path, "r") as f:
        config_content = json.load(f)
        print(config_content, type(config_content))
        return config_content


msg_matcher = on_message()

pgsql = get_config()


async def group_info(bot: Bot, groupId):
    """
    获取群信息，可以获取群名
    :param bot:
    :param groupId:
    :return:
    """
    groupInfo = await bot.get_group_info(group_id=groupId)
    return groupInfo


async def executeSql(sql):
    """
    异步执行sql
    :param sql:
    :return:
    """
    conn = await asyncpg.connect(user=pgsql["user"], password=pgsql["password"], database=pgsql["database"],
                                 host=pgsql["host"])
    # print("conn:", conn)
    await conn.execute(sql)
    await conn.close()


async def send_private(bot: Bot, user_id, msg):
    """
    发送私聊信息
    :param bot:
    :param user_id:
    :param msg:
    :return:
    """
    await bot.send_private_msg(user_id=user_id, message=str(msg))


@msg_matcher.handle()
async def saveMsg(bot: Bot, event: GroupMessageEvent):
    """
    保存群信息
    :param bot:
    :param event:
    :return:
    """
    msg = event
    print("msg:", msg)
    print(msg.get_message)
    # await send_private(bot, user_id=281016636, msg=msg)
    groupInfo = await group_info(bot, groupId=msg.group_id)
    dateArray = datetime.datetime.utcfromtimestamp(msg.time + 8 * 3600)  # 时区加8)
    msg_time = dateArray.strftime("%Y-%m-%d %H:%M:%S")
    sql = """INSERT INTO "public"."group"("message_id", "sender_name", "sender_id", "message", "group_id",
     "group_name", "group_card", "timestamp", "self_id", "post_type") 
     VALUES 
     ({0}, '{1}', {2}, '{3}', {4}, '{5}', '{6}', '{7}', {8}, '{9}');
""".format(msg.message_id, msg.sender.nickname, msg.sender.user_id, str(msg.message), msg.group_id,
           groupInfo["group_name"],
           msg.sender.card, msg_time, msg.self_id, msg.post_type)
    try:
        await executeSql(sql)
    except:
        print(sql)
        await send_private(bot, pgsql["user_id"], sql)  # 如果保存失败，把sql发送到指定的qq号
