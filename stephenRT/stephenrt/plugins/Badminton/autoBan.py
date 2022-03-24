#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/3/24 12:09
# @Author   : StephenZ
# @Site     : 
# @File     : autoBan.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>


import time, re, requests, json
import asyncio
import stephenrt.privateCfg as cfg
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText

from nonebot.permission import SUPERUSER
from nonebot import get_bot
from nonebot import on_metaevent

config = cfg.config_content

env = "prod"  # 根据环境读取配置

if env == "test":
    manager_base = config["manager_test"]
    user = config["manager_test_auth"]
else:
    manager_base = config["manager_prod"]
    user = config["manager_prod_auth"]

base_url = manager_base + "/login"
chat_url = manager_base + "/badmintonCn/getChatRoomMsg"
# ban_url = manager_base + "/badmintonCn/user_search_forbidden"

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

print("自动禁言脚本---------------------------------")


async def get_chats():
    payload = {}
    try:
        with requests.session() as session:
            session.post(url=base_url, data=user, headers=headers)
            response = session.post(url=chat_url, data=payload, headers=headers)
    except Exception as e:
        return str(e)
    return json.loads(response.content)


def filter_chat(chats_list):
    for chat in chats_list:
        if re.match("boxer_", chat["sendMan"]["name"]) and chat["isJy"] is False:
            # print("4399未禁言")
            if chat["sendType"] == "字符串" and len(chat["sendContent"]) > 10:
                # print("疑似广告")
                if "钻" in chat["sendContent"] and "S" in chat["sendContent"]:
                    result = "chatRoom疑似广告：" + str(chat["sendMan"]["numberUserId"]) + " " + chat["sendMan"][
                        "name"] + " " + \
                             chat["sendContent"].replace("\n", "")
                    return result


def test_chat(chat_list):
    for chat in chat_list:
        if "pk" in chat["sendContent"].lower():
            return chat["sendContent"]


async def send_message(msg):
    bot = get_bot()
    try:
        await bot.send_group_msg(group_id=792627520, message=str(msg))
    except Exception as e:
        await bot.send_private_msg(user_id=281016636, message=str(e))


# while True:
#     response = get_chats()
#     if response["status"] == 200:
#         chats = response["data"]
#         result = filter_chat(chats)
#         if result:
#             print(result)
#             # send_message(result)
#         time.sleep(10)

async def main():
    sent = []
    while True:
        response = await get_chats()
        if response["status"] == 200:
            chats = response["data"]
            result = filter_chat(chats)
            if result and result not in sent:
                print(result)
                sent.append(result)
                print(sent)
                # try:
                #     await bot.send_private_msg(user_id=281016636, message=str(result))
                # except Exception as e:
                #     await bot.send_private_msg(user_id=281016636, message=str(e))
            time.sleep(10)
            # asyncio.sleep(10)


# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# loop.close()

matcher = on_metaevent()
sent = []


@matcher.handle()
async def shut_user():
    bot = get_bot()
    response = await get_chats()
    print(json.dumps(response))
    if response["status"] == 200:
        chats = response["data"]
        result = test_chat(chats)
        if result and result not in sent:
            print(result)
            sent.append(result)
            try:
                # await bot.send_private_msg(user_id=281016636, message=str(result))
                await bot.send_group_msg(group_id=792627520, message=str(result))
            except Exception as e:
                await bot.send_private_msg(user_id=281016636, message=str(result) + str(e))
        # await asyncio.sleep(10)
