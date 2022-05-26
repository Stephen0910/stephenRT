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
import asyncio, time
import stephenrt.privateCfg as cfg
import websockets
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText

from nonebot.permission import SUPERUSER
from nonebot import get_bot
from nonebot import on_metaevent
import socket

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

socket_url = config["socket_url"]
base_url = manager_base + "/login"
chat_url = manager_base + "/badmintonCn/getChatRoomMsg"
# ban_url = manager_base + "/badmintonCn/user_search_forbidden"

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

text_check = ["鉆|钻|砖|钴|万|萬|澫", "s|元|沅|钱|q|秋秋|亓"]
name_check = ["3564837153|2580237802|166345259|3569544846|2927295662|1327004801|万钻|万钴|万砖|万鉆|萬鉆|萬钻|s级|s拍|亓|转石|鉆|钻|砖|钴"]

print("自动禁言脚本---------------------------------")


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


async def socket_message():
    print("获取房间信息websocket")
    msg_list = []
    async with websockets.connect(socket_url) as socket:
        for i in range(20):
            recieve = await socket.recv()
            msg_list.append(json.loads(recieve))
    # print("msg_list:", msg_list)
    return msg_list


async def get_chats():
    payload = {}
    try:
        with requests.session() as session:
            session.post(url=base_url, data=user, headers=headers)
            response = session.post(url=chat_url, data=payload, headers=headers)
    except Exception as e:
        return str(e)
    return json.loads(response.content)  # 延迟1条 否则还没来的


# 改版websocket 废弃
def filter_chat(chats_list):
    # for chat in chats_list[3:]:  # 延迟3条避免还没来得及自动禁
    for chat in chats_list[3:]:
        if re.match("[a-z]+\d+", chat["sendMan"]["name"]) or re.match("boxer_", chat["sendMan"]["name"]):
            if chat["isJy"] is False and chat["isFh"] is False:  # 是否已禁言开关
                if len(chat["sendContent"]) > 9:
                    # if "钻" or "砖" or "鉆" in chat["sendContent"] and "s" in chat["sendContent"].lower():
                    if re.search("鉆|钻|砖|钴|万|萬|澫", str(chat["sendContent"])) and re.search("s|元|沅|钱|q|秋秋",
                                                                                          str(chat[
                                                                                                  "sendContent"]).lower()) and \
                            chat["sendMan"]["rankStage"] == 1:
                        result = "chatRoom疑似广告：" + str(chat["sendMan"]["numberUserId"]) + " " + str(chat["sendMan"][
                                                                                                        "name"]) + " " + str(
                            chat["sendContent"]).replace("\n", "")
                        return result
                    elif re.match("3564837153|2580237802|166345259|3569544846|2927295662|1327004801|万钻|万钴|万砖|万鉆|萬鉆|萬钻",
                                  str(chat["sendMan"]["name"])):
                        result = "chatRoom疑似广告：" + str(chat["sendMan"]["numberUserId"]) + " " + str(chat["sendMan"][
                                                                                                        "name"]) + " " + str(
                            chat["sendContent"]).replace("\n", "")
                        return result


async def check_room():
    chat_msg = await socket_message()
    # print("chat_msg:", chat_msg)
    print(type(chat_msg))
    for chat in chat_msg:
        if chat["sendMan"]["rankStage"] == 1 and len(chat["sendContent"]) > 9:
            print(str(chat["sendMan"]["name"]).lower(), chat["sendContent"])
            print("大于9疑似")
            if re.search(text_check[0], str(chat["sendContent"]).lower()) and re.search(text_check[1], str(chat["sendContent"]).lower()) and re.match(
                "[a-z]+|\d+", chat["sendMan"]["name"]):
                result = "chatRoom发言广告：" + str(chat["sendMan"]["numberUserId"]) + " " + str(chat["sendMan"][
                                                                                                "name"]) + " " + str(
                    chat["sendContent"]).replace("\n", "")
                if chat["isJy"] is False and chat["isFh"] is False:  # 是否已禁言
                    print("result:", result)
                    return result
                else:
                    print("已经禁言了")
            elif re.search(name_check[0], str(chat["sendMan"]["name"]).lower()) and len(
                    chat["sendMan"]["name"]) > 8:
                result = "chatRoom名字广告：" + str(chat["sendMan"]["numberUserId"]) + " " + str(chat["sendMan"][
                                                                                                "name"]) + " " + str(
                    chat["sendContent"]).replace("\n", "")
                if chat["isJy"] is False and chat["isFh"] is False:
                    return result
                else:
                    print("已经禁言了")
            else:
                print("不处理：", name_check[0], text_check)


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


matcher = on_metaevent()

block_list = []


@matcher.handle()
async def shut_user():
    bot = get_bot()
    try:
        result = await check_room()
        print("---result-----", result)
        if result != None and result not in block_list:
            print("检测到：", result)
            block_list.append(result)
            try:
                # await bot.send_private_msg(user_id=281016636, message=str(result))
                # if get_host_ip() == "10.10.10.8":
                if result:
                    print("8号机发送消息")
                    await bot.send_group_msg(group_id=group_id, message=str(result))
            except Exception as e:
                await bot.send_private_msg(user_id=user_id, message=str(result) + str(e))
            finally:
                print("block_list:", block_list)

    except Exception as e:
        result = "获取消息列表失败：" + str(e)
        print(result)

    # if len(block_list) > 3:
    #     pass
    #     block_list = block_list[:1]

    # await asyncio.sleep(10)
