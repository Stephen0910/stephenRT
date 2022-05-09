#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/1/29 16:14
# @Author   : StephenZ
# @Site     : 
# @File     : __init__.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Event
from nonebot import on_message
import asyncpg
import json
import os
import time, datetime, sys
import re

# import stephenRT.stephenrt.privateCfg as cfg
sys.path.append("../../")
import stephenrt.privateCfg as cfg

# def get_config():
#     """
#     配置数据库信息和收取保存失败的qq号
#     :return:
#     """
#     up_dir = os.path.abspath(os.path.join(os.getcwd(), "../../"))
#     config_path = os.path.join(up_dir, "config.json")
#     with open(config_path, "r") as f:
#         config_content = json.load(f)
#         # print(config_content, type(config_content))
#         return config_content


msg_matcher = on_message()

pgsql = cfg.config_content


async def group_info(bot: Bot, groupId):
    """
    获取群信息，可以获取群名
    :param bot:
    :param groupId:
    :return:
    """
    groupInfo = await bot.get_group_info(group_id=groupId)
    return groupInfo


async def get_mems(bot:Bot, groupId):
    mems = await bot.get_group_member_list(group_id=groupId)
    return mems

async def executeSql(sql):
    """
    异步执行插入sql
    :param sql:
    :return:
    """
    conn = await asyncpg.connect(user=pgsql["user"], password=pgsql["password"], database=pgsql["database"],
                                 host=pgsql["host"])
    # print("conn:", conn)
    await conn.execute(sql)
    await conn.close()


async def poolSave(sql):
    """
    连接池
    :param sql:
    :return:
    """
    pool = await asyncpg.create_pool(user=pgsql["user"], password=pgsql["password"], database=pgsql["database"],
                                     host=pgsql["host"])
    for i in range(1, 1000):
        async with pool.acquire() as con:
            # await con.fetchval('select 2 ^ $1', power)
            await con.execute(sql)
    await pool.close()


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
    # print("msg:", msg)
    get_type = msg.get_type
    print("get_type:", type(get_type), get_type)
    try:
        msg_type = str([x[2:] for x in re.findall("=\'text|=\'image|=\'json|=\'face", str(get_type))]).replace("'", "\"")
    except Exception as e:
        print(e)
        msg_type = ""
    print("msg_type:", msg_type, type(msg_type))
    # print(msg.message["type"])
    # await send_private(bot, user_id=281016636, msg=msg)
    groupInfo = await group_info(bot, groupId=msg.group_id)
    dateArray = datetime.datetime.utcfromtimestamp(msg.time)  # 时区加8 不加了
    msg_time = dateArray.strftime("%Y-%m-%d %H:%M:%S")
    sql = """INSERT INTO "public"."group"("message_id", "sender_name", "sender_id", "message", "group_id",
     "group_name", "group_card", "timestamp", "self_id", "post_type", "msg_type") 
     VALUES 
     ({0}, '{1}', {2}, '{3}', {4}, '{5}', '{6}', '{7}', {8}, '{9}', '{10}');
""".format(msg.message_id, str(msg.sender.nickname).replace("\'", "\""), msg.sender.user_id,
           str(msg.message).replace("\'", "\""), msg.group_id,
           groupInfo["group_name"],
           str(msg.sender.card).replace("\'", "\""), msg_time, msg.self_id, msg.post_type, msg_type)

    # await poolSave(sql)

    # mem1 = str(bot.get_group_member_list(612610584))
    # mem2 = str(bot.get_group_member_list(310100922))
    # mem1 = await get_mems(bot, groupId=612610584)
    # mem2 = await get_mems(bot, groupId=310100922)
    #
    # print("mmmmmmmmmmmmmmmmmm2:")
    # print(mem2)
    #
    # test_file = "/home/a.txt"
    # if os.path.exists(test_file) is False:
    #     with open(test_file, "a+") as f:
    #         f.write(mem2)


    try:
        await executeSql(sql)

        # print(bot.get_group_member_list(group_id=612610584))



        # print(bot.get_group_member_list(group_id=612610584))
        # await poolSave(sql)
    except Exception as e:
        print(sql)
        await send_private(bot, pgsql["user_id"], e)  # 如果保存失败，把sql发送到指定的qq号



# export = export()
# export.config = pgsql
