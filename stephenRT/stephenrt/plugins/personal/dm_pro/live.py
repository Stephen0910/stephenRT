#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/5/24 14:53
# @Author   : StephenZ
# @Site     : 
# @File     : live.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>


import requests
import json
import time, re, requests, json
import asyncio, time
import stephenrt.privateCfg as cfg
import websockets
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from lxml import etree
from nonebot.permission import SUPERUSER
from nonebot import get_bot
from nonebot import on_metaevent
from nonebot.params import Depends
from nonebot.adapters.onebot.v11.message import MessageSegment

rooms = {"5645739": "a824683653", "5264153": "肖璐s", "5106536": "599"}
show_status = {"0": "等待开播", "1": "直播中", "2": "直播结束"}


def get_mc():
    url = "https://www.doseeing.com/rank/chat/7day?category=9"
    content_num = 8
    mc_dict = {}
    with requests.get(url) as session:
        page_html = etree.HTML(session.content)
        text_list = page_html.xpath("/html/body/div/div[2]/main/div/div/div[2]/table[2]/tbody//text()")
        mc_num = int(len(text_list) / content_num)
        for i in range(mc_num):
            if text_list[i * content_num + 3] == "DOTA":
                room = page_html.xpath(
                    "/html/body/div/div[2]/main/div/div/div[2]/table[2]/tbody/tr[{0}]/td[2]/a/@href".format(i + 1))
                room_id = re.search("\d+", str(room)).group()
                mc_dict[text_list[i * content_num + 1]] = room_id
    return mc_dict


def new_id(old_id):
    url = "https://www.douyu.com/{0}".format(old_id)
    with requests.get(url) as session:
        page_html = etree.HTML(session.content)
        redict_url = page_html.xpath("/html/body/section/main/div[4]/div[1]/div[1]/div[1]/div[1]/div/a/@href")
        room_id = re.search("\d+\d", str(redict_url)).group()
    return room_id


def first_response():
    print("run first_response---------")
    mcs = get_mc()
    info = "请输入要查询的主播信息（输入以下序号或房间号）:\n"
    index = 1
    for key, value in mcs.items():
        msg_dict = room_status(value)
        if msg_dict["is_alive"] == 0:
            status = "未直播"
        elif msg_dict["is_alive"] == 2:
            status = "直播结束"
        elif msg_dict["is_alive"] == 1 and msg_dict["is_loop"] == 1:
            status = "录播中"
        elif msg_dict["is_alive"] == 1 and msg_dict["is_loop"] == 0:
            status = "直播中"

        info = info + "{0}、{1}\n".format(index, key)
        index += 1
    return info


# 非异步
def room_status(room_id):
    url = "https://www.douyu.com/betard/{0}".format(room_id)
    payload = {}
    headers = {}
    with requests.get(url=url, headers=headers, data=payload) as session:
        # print(session.text)
        data = json.loads(str(session.text))
        try:
            child_cate = data["game"]["tag_name"]
        except Exception as e:
            child_cate = ""
            # print(e)
        room_info = data["room"]
        is_alive = room_info["show_status"]  # 是否在播
        nickname = room_info["nickname"]
        if room_info["authInfo"]["type"] == 1:
            auth = room_info["authInfo"]["desc"]
        elif room_info["authInfo"]["type"] == 0:
            auth = ""
        # small_avatar = room_info["avatar"]["small"]
        owner_avatar = room_info["avatar"]["small"]
        room_name = room_info["room_name"]
        level_info = room_info["levelInfo"]
        # room_src = "https://rpic.douyucdn.cn/" + room_info["room_src"]
        room_pic = room_info["room_pic"]
        hot = room_info["room_biz_all"]["hot"]
        end_time = room_info["end_time"]
        is_loop = room_info["videoLoop"]
        second_lvl_name = room_info["second_lvl_name"]
        if room_info["fans_bn"] is False:
            fans_bn = ""
        else:
            fans_bn = json.loads(room_info["fans_bn"])["bn"]

        primary = {
            "child_cate": child_cate, "nickname": nickname, "owner_avatar": owner_avatar, "is_alive": is_alive,
            "hot": hot, "room_name": room_name, "room_pic": room_pic, "fans_bn": fans_bn, "is_loop": is_loop,
            "auth": auth
        }
        # print(child_cate)
        # print(nickname, owner_avatar, is_alive, "热度：", hot)
        # print(room_name, "房间图片：", room_pic)
        # print("牌子：", fans_bn)
        # print("是否录播:", is_loop)
        # print(auth)
        # print("\n\n--------------------------")
        return primary


async def get_roomInfo(room_id):
    url = "https://www.douyu.com/betard/{0}".format(room_id)
    payload = {}
    headers = {}
    with requests.get(url=url, headers=headers, data=payload, allow_redirects=True) as session:
        # print(session.text)
        data = json.loads(str(session.text))
        try:
            child_cate = data["game"]["tag_name"]
        except Exception as e:
            child_cate = ""
            print(e)
        room_info = data["room"]
        is_alive = room_info["show_status"]  # 是否在播
        nickname = room_info["nickname"]
        if room_info["authInfo"]["type"] == 1:
            auth = room_info["authInfo"]["desc"]
        elif room_info["authInfo"]["type"] == 0:
            auth = ""
        # small_avatar = room_info["avatar"]["small"]
        owner_avatar = room_info["avatar"]["small"]
        room_name = room_info["room_name"]
        level_info = room_info["levelInfo"]
        # room_src = "https://rpic.douyucdn.cn/" + room_info["room_src"]
        room_pic = room_info["room_pic"]
        hot = room_info["room_biz_all"]["hot"]
        end_time = room_info["end_time"]
        is_loop = room_info["videoLoop"]
        second_lvl_name = room_info["second_lvl_name"]
        if room_info["fans_bn"] is False:
            fans_bn = ""
        else:
            fans_bn = json.loads(room_info["fans_bn"])["bn"]

        primary = {
            "child_cate": child_cate, "nickname": nickname, "owner_avatar": owner_avatar, "is_alive": is_alive,
            "hot": hot, "room_name": room_name, "room_pic": room_pic, "fans_bn": fans_bn, "is_loop": is_loop,
            "auth": auth
        }
        # print(child_cate)
        # print(nickname, owner_avatar, is_alive, "热度：", hot)
        # print(room_name, "房间图片：", room_pic)
        # print("牌子：", fans_bn)
        # print("是否录播:", is_loop)
        # print(auth)
        # print("\n\n--------------------------")
        return primary


dy = on_command("dy", rule=to_me(), aliases={"douyu", "直播", "zhibo", "zb"}, priority=1, permission=SUPERUSER)

first_msg = []
first_msg.append(first_response())  # 临时处理方案


@dy.handle()
async def msg_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  #
    if plain_text:
        matcher.set_arg("room_id", args)  # 如果用户发送了参数则直接赋值


async def depend():
    info = first_response()
    return info


@dy.got("room_id", prompt=first_response())
async def get_live(
        room_id: Message = Arg()
):
    room_id = str(room_id)
    # print("room_id:", room_id)
    if not re.search("^\d+$", room_id):
        await dy.finish("输入的不是直播间号， 结束会话")

    mcs = get_mc()
    # print(mcs)
    if int(room_id) < len(mcs) + 1:
        room_id = list(mcs.values())[int(room_id) - 1]
        msg_dict = await get_roomInfo(room_id)

    # elif room_id == "90016":
    #     msg_dict = await get_roomInfo(532152)
    else:
        try:
            msg_dict = await get_roomInfo(room_id)
        except:
            msg_dict = await get_roomInfo(new_id(room_id))

    if msg_dict["is_alive"] == 0:
        status = "未直播"
    elif msg_dict["is_alive"] == 2:
        status = "直播结束"
    elif msg_dict["is_alive"] == 1 and msg_dict["is_loop"] == 1:
        status = "录播中"
    elif msg_dict["is_alive"] == 1 and msg_dict["is_loop"] == 0:
        status = "直播中"
    else:
        status = "状态未知"
    live_pic = msg_dict["room_pic"]
    live_pic = MessageSegment.image(live_pic)
    avatar = MessageSegment.image(msg_dict["owner_avatar"])
    msg = avatar + "{4}\n⬤  【{0}】\n⬤  {1}\n⬤  {2}\n⬤  热度：{3}".format(msg_dict["nickname"], msg_dict["room_name"],
                                                                     status,
                                                                     msg_dict["hot"], msg_dict["child_cate"]) + live_pic

    await dy.finish(msg)


def rooms_states():
    room_states = {}
    for key, value in rooms.items():
        room_info = room_status(key)
        is_alive = room_info["is_alive"]
        is_loop = room_info["is_loop"]

        if is_alive in [0, 2]:
            status = "未直播"
        elif is_alive == 1 and is_loop == 1:
            status = "录播中"
        elif is_alive == 1 and is_loop == 0:
            status = "直播中"
        else:
            status = "状态未知"
        room_states[key] = status
    return room_states


live_msg = on_metaevent()
first_states = rooms_states()

@live_msg.handle()
async def live_notifacation():
    bot = get_bot()
    states = rooms_states()
    for key, value in states.items():
        if first_states[key] == "未直播" and value == "直播中":
            msg_dict = await get_roomInfo(key)
            if msg_dict["is_alive"] == 0:
                status = "未直播"
            elif msg_dict["is_alive"] == 2:
                status = "直播结束"
            elif msg_dict["is_alive"] == 1 and msg_dict["is_loop"] == 1:
                status = "录播中"
            elif msg_dict["is_alive"] == 1 and msg_dict["is_loop"] == 0:
                status = "直播中"
            else:
                status = "状态未知"
            live_pic = msg_dict["room_pic"]
            live_pic = MessageSegment.image(live_pic)
            avatar = MessageSegment.image(msg_dict["owner_avatar"])

            msg = avatar + "{4}\n⬤  【{0}】\n⬤  {1}\n⬤  {2}\n⬤  热度：{3}".format(msg_dict["nickname"], msg_dict["room_name"],
                                                                     status,
                                                                     msg_dict["hot"], msg_dict["child_cate"]) + live_pic
            await bot.send_private_msg(user_id=281016636, message=msg)


        elif first_states[key] == "直播中" and value == "未直播":
            msg_dict = await get_roomInfo(key)
            msg = "{0} 下播了".format(msg_dict["nickname"])
            await bot.send_private_msg(user_id=281016636, message=msg)

        first_states[key] = value






