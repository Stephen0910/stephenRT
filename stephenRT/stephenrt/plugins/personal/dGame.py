#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/4/11 9:20
# @Author   : StephenZ
# @Site     : 
# @File     : dGame.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import requests, json
import urllib, time
from nonebot import on_metaevent
from nonebot import get_bot
import re
import asyncio
import socket
from nonebot.adapters.onebot.v11.message import MessageSegment


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


header = {"Content-Type": "application/json"}


def get_ids():
    names = ["你好尹天仇", "宁心之殇", "晴天眼神", "上海康恒", "再见柳飘飘", "求坑丶"]
    id_url = "https://users.09game.com/home/GetUserPub?user_name="
    ids = {}
    for name in names:
        url_name = urllib.parse.quote("\'" + name + "\'")
        response = requests.get(id_url + url_name).text
        id = json.loads(response)["temp"][0]["user_id"]
        ids[name] = id
    print(ids)
    return ids


async def get_recent_data(id):
    recent_url = "https://score.09game.com/MOBA/BasicDataList?UserID={0}&GameTypeID=21&CurrentSeason=0&GameSource=-1&Time=-1&PageIndex=0&PageSize=6".format(
        str(id))
    response = requests.get(recent_url)
    content = json.loads(response.content)
    last_game = content["data"]["listEntity"][0]
    await asyncio.sleep(15)
    return last_game


async def get_dg_id(id):
    id_url = "https://score.09game.com/RPG/GameList?UserID={0}&GameTypeID=142&GameSource=-1&Type=2&Number=11".format(id)
    response = requests.get(id_url)
    content = json.loads(response.content)
    last_game = content["data"][0]
    await asyncio.sleep(15)
    return last_game


def get_msg():
    pass


ids = get_ids()
# print(get_recent_data(369818))


matcher = on_metaevent()

if get_host_ip() == "10.10.10.8":
    first_time = int(time.time())
    group = 959822848
else:
    # first_time = 1
    first_time = int(time.time())
    group = 755489024

print("first_time:", first_time)
time_list = [first_time]


@matcher.handle()
async def game_info():
    bot = get_bot()
    g_ids = []
    o_msg = ""
    d_msg = ""
    for name, id in ids.items():
        data = await get_recent_data(id)
        create_time = data["create_time"]
        g_id = data["g_id"]
        g_source = data["g_source"]
        t_create_time = int(time.mktime(time.strptime(create_time, "%Y-%m-%dT%H:%M:%S")))
        # print(t_create_time)
        if t_create_time > time_list[-1]:
            g_ids.append(g_id)
            time_list.append(t_create_time)
            break
        # else:
        #     print(t_create_time)

    if len(g_ids) > 0:
        new_id = g_ids[0]
        is_win = "OMG 胜" if data["game_result"] == "0" else "OMG 负"
        id_url = "https://score.09game.com/MOBA/CorrelationPlayerMilitaryExploit?GameTypeID=21&GameID={0}&GameSource={1}&CurrentSeason=0".format(
            new_id, g_source)
        # ima_url = "https://www.09game.com/html/2020gamescore/web/gamedetail/21.html?sessid=0&gameid={0}".format(
        #     new_id)
        # print("ima_url:", ima_url)
        # image = MessageSegment.image(file=ima_url)
        omg_spend = int(data["time_length"]) // 60 + 1
        detail = json.loads(requests.get(id_url).content)
        print("执行omg具体信息")
        # print(json.dumps(detail))
        for data in detail["data"]:
            if data["user_name"] in ids.keys():
                kda = "{0}/{1}/{2}".format(data["kill_count"], data["killed_count"], data["assist_count"])
                hero_name, hero_level = data["hero_name"], data["hero_level"]
                omg_msg = is_win + " {0}分钟\n".format(omg_spend) + name + "-" + hero_name + ":" + kda + "\n"
                # print(omg_msg)
                o_msg += omg_msg
        print(o_msg)
        if len(o_msg) > 5:
            try:
                await bot.send_group_msg(group_id=group, message=o_msg)
            except Exception as e:
                await bot.send_private_msg(user_id=281016636, message=str(o_msg) + str(e))

            # try:
            #     await bot.send_group_msg(group_id=group, message=image)
            # except Exception as e:
            #     await bot.send_private_msg(user_id=281016636, message=image)

    else:
        print("OMG无")

    # DG
    dg_ids = []
    for name, id in ids.items():
        try:
            dg_data = await get_dg_id(id)

        except:
            dg_data = "无"  # 没有对局
            continue
        dg_create_time = dg_data["create_time"]
        dg_id = dg_data["game_id"]
        dg_create_time = int(time.mktime(time.strptime(dg_create_time, "%Y-%m-%dT%H:%M:%S")))
        # print(dg_create_time)
        if dg_create_time > time_list[-1]:
            dg_ids.append(dg_id)
            time_list.append(dg_create_time)
            break

    if len(dg_ids) > 0:
        new_id = dg_ids[0]
        is_win = "龙魂 胜" if dg_data["game_result"] == "0" else "龙魂 负"
        id_url = "https://score.09game.com/RPG/GamePerformanceListJson?GameTypeID=142&gameid={0}&gamesource=".format(
            new_id)
        # ima_url = "https://www.09game.com/html/2020gamescore/web/gamedetail/142.html?userid={0}&gameid={1}".format(id,
        #                                                                                                    new_id)
        # image = MessageSegment.image(file=ima_url)
        dg_spend = int(dg_data["time_length"]) // 60 + 1
        dg_detail = json.loads(requests.get(id_url).content)
        print("执行dg具体信息")
        for data in dg_detail["data"]:
            if data["user_name"] in ids.keys():
                kda = re.match("击杀:\d+;死亡:\d+;助攻:\d+;", data["extra_value"]).group()
                dg_msg = is_win + " {0}分钟\n".format(dg_spend) + data["user_name"] + ":" + kda + "\n"
                print(dg_msg)
                d_msg += dg_msg

        if len(d_msg) > 5:
            try:
                await bot.send_group_msg(group_id=group, message=d_msg)
            except Exception as e:
                await bot.send_private_msg(user_id=281016636, message=str(d_msg) + str(e))

            # try:
            #     await bot.send_group_msg(group_id=group, message=image)
            # except Exception as e:
            #     await bot.send_private_msg(user_id=281016636, message=image)


# print(get_recent_data(369818))
# print(get_dg_id(369818))
