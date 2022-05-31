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


import requests, datetime
import json
import time, re, requests, json
import asyncio, time
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

import urllib3

urllib3.disable_warnings()
requests.adapters.DEFAULT_RETRIES = 5

print("live loading")

rooms = {"5645739": "a824683653", "5264153": "肖璐s", "5106536": "599", "6566346": "paogod"}
show_status = {"0": "等待开播", "1": "直播中", "2": "直播结束"}

dosee_headers = {
    "host": "www.doseeing.com",
    "method": "GET",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-GB,en;q=0.9",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}


def get_mc():
    content_num = 8
    mc_dict = {}
    payload = {}
    for i in [1, 2]:
        url = "https://www.doseeing.com/rank/chat/7day?category=9&p={0}".format(i)
        try:
            with requests.get(url, headers=dosee_headers, data=payload, verify=False) as session:
                page_html = etree.HTML(session.content)
                text_list = page_html.xpath("/html/body/div/div[2]/main/div/div/div[2]/table[2]/tbody//text()")
                mc_num = int(len(text_list) / content_num)
                for i in range(mc_num):
                    if text_list[i * content_num + 3] == "DOTA":
                        room = page_html.xpath(
                            "/html/body/div/div[2]/main/div/div/div[2]/table[2]/tbody/tr[{0}]/td[2]/a/@href".format(i + 1))
                        room_id = re.search("\d+", str(room)).group()
                        mc_dict[text_list[i * content_num + 1]] = room_id
        except:
            mc_dict = ""
    return mc_dict


def new_id(old_id):
    url = "https://www.douyu.com/{0}".format(old_id)
    with requests.get(url, headers=dy_headers, verify=False, timeout=3) as session:
        page_html = etree.HTML(session.content)
        redict_url = page_html.xpath("/html/body/section/main/div[4]/div[1]/div[1]/div[1]/div[1]/div/a/@href")
        room_id = re.search("\d+\d", str(redict_url)).group()
    return room_id


def first_response():
    split_symbol = "⬤"
    print("run first_response---------")
    mcs = get_mc()
    # info = "请输入要查询的主播信息（输入以下序号或房间号）:\n"
    info = "斗鱼DOTA1七日弹幕排行：\n"
    index = 1
    for key, value in mcs.items():
        if index < 11:
            msg_dict = room_status(value)
            if msg_dict["is_alive"] == 0:
                status = "未直播"
            elif msg_dict["is_alive"] == 2:
                status = "直播结束"
            elif msg_dict["is_alive"] == 1 and msg_dict["is_loop"] == 1:
                status = "录播中"
            elif msg_dict["is_alive"] == 1 and msg_dict["is_loop"] == 0:
                status = "直播中"

            if msg_dict["is_alive"] in [0, 2]:
                info = info + "{4}  {0}、{1} [{2}]  {3}\n".format(index, key, value, status, split_symbol)
            else:
                info = info + "{5}  {0}、{1} [{2}] {3}  热度:{4} \n".format(index, key, value, status, msg_dict["hot"],
                                                                         split_symbol)
            index += 1
        else:
            break
    return info


dy_headers = {
    "method": "GET",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-GB,en;q=0.9",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
}


# 非异步
def room_status(room_id):
    url = "https://www.douyu.com/betard/{0}".format(room_id)
    payload = {}
    try:
        with requests.get(url=url, headers=dy_headers, data=payload, verify=False, timeout=1) as session:
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
            owner_avatar = room_info["avatar"]["middle"]
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

    except:
        primary = "查询失败"
    return primary


async def dosee_info(id):
    d1 = "https://www.doseeing.com/data/api/topuser/{0}?type=gift&dt=0".format(id)
    d2 = "https://www.doseeing.com/data/api/topuser/{0}?type=chat&dt=0".format(id)
    with requests.get(d1, verify=False, timeout=3) as session:
        if session.status_code == 200:
            response = json.loads(session.text)["data"]

            pay = "今日付费排行：\n" + "".join(
                [str(x["rank"]) + ": " + x["user.nickname"] + " ￥{0}".format(x["gift.paid.price"] / 100) + "\n" for x in
                 response if x["rank"] < 4])
            print(pay)
    with requests.get(d2, verify=False, timeout=3) as session:
        if session.status_code == 200:
            response = json.loads(session.text)["data"]
            talk = "今日弹幕排行: \n" + "".join(
                [str(x["rank"]) + ":" + x["user.nickname"] + " {0} 条".format(x["chat.pv"]) + "\n" for x in response if
                 x["rank"] < 4])
            print(talk)

    return pay + talk + "-"*20 + "\n"


async def get_roomInfo(room_id):
    url = "https://www.douyu.com/betard/{0}".format(room_id)
    payload = {}
    headers = {}
    with requests.get(url=url, headers=headers, data=payload, allow_redirects=True, timeout=3, verify=False) as session:
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


mcs = get_mc()

prompt = "⬤  输入要查询直播间号(或前十序号)\n⬤  0为获取榜单前十"


@dy.got("room_id", prompt=prompt)
async def get_live(
        room_id: Message = Arg()
):
    room_id = str(room_id)

    if not re.search("^\d+$", room_id):
        await dy.finish("输入的不是直播间号， 结束会话")

    if room_id == "0":
        await dy.finish(first_response())

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
            room_id = new_id(room_id)
            msg_dict = await get_roomInfo(room_id)

    try:
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
        today = await dosee_info(room_id)
        msg = avatar + today + "{4}\n⬤  {0}\n⬤  {1}\n⬤  {2}\n⬤  热度：{3}".format(msg_dict["nickname"], msg_dict["room_name"],
                                                                       status,

                                                                       msg_dict["hot"],
                                                                       msg_dict["child_cate"]) + live_pic
    except Exception as e:
        msg = "查询失败：{0}".format("请重试")
        print(str(e))
    print("sent:", msg)
    await dy.finish(msg)


def first_states():
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
    print("first_states():", room_states)
    return room_states


async def rooms_states():
    """
    异步获取房间信息
    :return:
    """
    room_states = {}
    for key, value in rooms.items():
        room_info = await get_roomInfo(key)
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
init_states = first_states()
trigger = 1

# init_states = {'5645739': '未直播', '5264153': '未直播', '5106536': '未直播', '6566346': '未直播'}


@live_msg.handle()
async def live_notifacation():
    global trigger
    if trigger % 3 == 0:
        bot = get_bot()
        try:
            states = await rooms_states()
        except:
            states = init_states  # 错误则使用初始
        for key, value in states.items():
            if init_states[key] == "未直播" and value == "直播中":
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

                dateArray = datetime.datetime.utcfromtimestamp(int(time.time() + 8 * 3600))
                msg_time = dateArray.strftime("%Y-%m-%d %H:%M:%S")
                msg = "上钟提醒-" + str(msg_time) + avatar + "{4}\n⬤  【{0}】\n⬤  {1}\n⬤  {2}\n⬤  热度：{3}".format(
                    msg_dict["nickname"],
                    msg_dict["room_name"],
                    status,
                    msg_dict["hot"],
                    msg_dict[
                        "child_cate"]) + live_pic
                init_states[key] = value
                await bot.send_private_msg(user_id=281016636, message=msg)

            elif init_states[key] == "直播中" and value == "未直播":
                msg_dict = await get_roomInfo(key)
                dateArray = datetime.datetime.utcfromtimestamp(int(time.time() + 8 * 3600))
                msg = "下钟提醒\n{0} 下播了".format(msg_dict["nickname"])
                init_states[key] = value
                await bot.send_private_msg(user_id=281016636, message=msg)
    else:
        print("live trigger pass:{0}".format(trigger))
    trigger += 1
