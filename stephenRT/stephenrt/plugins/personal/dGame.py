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
import urllib, time, random
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Event
from nonebot import on_metaevent
from nonebot import get_bot
from nonebot import on_message
import re

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


def get_recent_data(id):
    recent_url = "https://score.09game.com/MOBA/BasicDataList?UserID={0}&GameTypeID=21&CurrentSeason=0&GameSource=-1&Time=-1&PageIndex=0&PageSize=6".format(
        str(id))
    response = requests.get(recent_url)
    content = json.loads(response.content)
    last_game = content["data"]["listEntity"][0]
    return last_game


def get_dg_id(id):
    id_url = "https://score.09game.com/RPG/GameList?UserID={0}&GameTypeID=142&GameSource=-1&Type=2&Number=11".format(id)
    response = requests.get(id_url)
    content = json.loads(response.content)
    last_game = content["data"][0]
    return last_game


def get_msg():
    pass


ids = get_ids()
# print(get_recent_data(369818))


matcher = on_metaevent()

global new_time
# first_time = 1649601176
first_time = int(time.time())
print("first_time:", first_time)
time_list = [first_time]


@matcher.handle()
async def game_info():
    bot = get_bot()
    g_ids = []
    omg_msg = ""
    dg_msg = ""
    for name, id in ids.items():
        data = get_recent_data(id)
        create_time = data["create_time"]
        g_id = data["g_id"]
        g_source = data["g_source"]
        t_create_time = int(time.mktime(time.strptime(create_time, "%Y-%m-%dT%H:%M:%S")))
        if t_create_time > time_list[-1]:
            g_ids.append(g_id)  # g_id存一起，要去重
            time_list.append(t_create_time)
            break
        # else:
        #     print(t_create_time)

    if len(g_ids) > 0:
        new_id = g_ids[0]
        is_win = "OMG胜" if data["game_result"] == "0" else "OMG负"
        id_url = "https://score.09game.com/MOBA/CorrelationPlayerMilitaryExploit?GameTypeID=21&GameID={0}&GameSource={1}&CurrentSeason=0".format(
            new_id, g_source)
        omg_spend = int(data["time_length"]) // 60 + 1
        detail = json.loads(requests.get(id_url).content)
        # print(json.dumps(detail))
        for data in detail["data"]:
            if data["user_name"] in ids.keys():
                kda = "{0}/{1}/{2}".format(data["kill_count"], data["killed_count"], data["assist_count"])
                hero_name, hero_level = data["hero_name"], data["hero_level"]
                # print(is_win, omg_spend)
                # print(name, hero_name, kda)
                omg_msg = is_win + " {0}分钟\n".format(omg_spend) + name + "-" + hero_name + ":" + kda
                # print(omg_msg)
                if omg_msg > 5:
                    try:
                        await bot.send_group_msg(group_id=959822848, message=omg_msg)
                    except Exception as e:
                        await bot.send_private_msg(user_id=281016636, message=str(omg_msg) + str(e))

    else:
        print("OMG无")

    # DG
    dg_ids = []
    for name, id in ids.items():
        try:
            dg_data = get_dg_id(id)

        except:
            dg_data = "无"  # 没有对局
            continue
        dg_create_time = dg_data["create_time"]
        dg_id = dg_data["game_id"]
        dg_create_time = int(time.mktime(time.strptime(dg_create_time, "%Y-%m-%dT%H:%M:%S")))
        # print(dg_create_time)
        if dg_create_time > time_list[-1]:
            dg_ids.append(dg_id)  # g_id存一起，要去重
            time_list.append(dg_create_time)
            break

    if len(dg_ids) > 0:
        new_id = dg_ids[0]
        is_win = "龙魂 胜" if dg_data["game_result"] == "0" else "龙魂 负"
        id_url = "https://score.09game.com/RPG/GamePerformanceListJson?GameTypeID=142&gameid={0}&gamesource=".format(
            new_id)
        dg_spend = int(dg_data["time_length"]) // 60 + 1
        dg_detail = json.loads(requests.get(id_url).content)
        for data in dg_detail["data"]:
            if data["user_name"] in ids.keys():
                kda = re.match("击杀:\d+;死亡:\d+;助攻:\d+;", data["extra_value"]).group()
                # print(is_win)
                # print(data["user_name"], dg_spend)
                # print(kda)
                dg_msg = is_win + " {0}分钟\n".format(dg_spend) + data["user_name"] + ":" + kda
                if omg_msg > 5:
                    try:
                        await bot.send_group_msg(group_id=959822848, message=dg_msg)
                    except Exception as e:
                        await bot.send_private_msg(user_id=281016636, message=str(omg_msg) + str(e))

    sleep = random.randint(50, 70)
    time.sleep(sleep)

# print(get_recent_data(369818))
# print(get_dg_id(369818))
