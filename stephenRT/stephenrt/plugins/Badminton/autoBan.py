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
group_id = config["group_id_badminton"]
user_id = config["user_id"]

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
    return json.loads(response.content)  # 延迟1条 否则还没来的


def filter_chat(chats_list):
    for chat in chats_list[2:]:  # 延迟1条避免还没来得及自动禁言
        # if re.match("boxer_", chat["sendMan"]["name"]):
        if re.match("boxer_", chat["sendMan"]["name"]):
            if chat["isJy"] is False and chat["isFh"] is False:
                if len(chat["sendContent"]) > 15:
                    # if "钻" or "砖" or "鉆" in chat["sendContent"] and "s" in chat["sendContent"].lower():
                    if re.search("鉆|钻|砖|钴", str(chat["sendContent"])) and re.search("s|元|沅", str(chat["sendContent"]).lower()):
                        result = "chatRoom疑似广告：" + str(chat["sendMan"]["numberUserId"]) + " " + str(chat["sendMan"][
                                                                                                        "name"]) + " " + str(
                            chat["sendContent"]).replace("\n", "") + str(chat["isFh"]) + str(chat["isJy"])
                        return result
        elif re.match("3564837153|166345259|3569544846|2927295662|万钻|万钴|万砖|万鉆", str(chat["sendMan"]["name"])):
            result = "chatRoom疑似广告：" + str(chat["sendMan"]["numberUserId"]) + " " + str(chat["sendMan"][
                                                                                            "name"]) + " " + str(
                chat["sendContent"]).replace("\n", "") + str(chat["isFh"]) + str(chat["isJy"])
            return result


def test_chat(chat_list):
    for chat in chat_list:
        if "部" in str(chat["sendContent"]).lower():
            return str(chat["sendMan"]["name"]) + "： " + str(chat["sendContent"])


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


matcher = on_metaevent()

block_list = []


@matcher.handle()
async def shut_user():
    bot = get_bot()

    response = await get_chats()
    if response["status"] == 200:
        chats = response["data"]
        result = filter_chat(chats)
        if result and result not in block_list:
            # print("检测到：", result)
            block_list.append(result)
            try:
                # await bot.send_private_msg(user_id=281016636, message=str(result))
                await bot.send_group_msg(group_id=group_id, message=str(result))
            except Exception as e:
                await bot.send_private_msg(user_id=user_id, message=str(result) + str(e))
            finally:
                print("block_list:", block_list)

    # if len(block_list) > 3:
    #     pass
    #     block_list = block_list[:1]

    # await asyncio.sleep(10)
