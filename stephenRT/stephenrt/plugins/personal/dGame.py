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

sleep_time = 5


def transfer_dId(id):
    id = int(id)
    if id <= 0:
        return 0
    t1 = id & 255
    t2 = id >> 8 & 255
    t3 = id >> 16 & 255
    t4 = id >> 24 & 255
    return chr(t4) + chr(t3) + chr(t2) + chr(t1)


def get_title(a):
    user_title = ""
    title_num = str(bin(a))[2:]
    for index, i in enumerate(title_num[::-1]):
        if i == "1":
            user_title += titles[index]
    return user_title


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


names = ["你好尹天仇", "宁心之殇", "晴天眼神", "上海康恒", "再见柳飘飘", "求坑丶", "CG控", "小灰灰居然"]

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "User_Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "Host": "score.09game.com"
}

game_source = {"0": "自由作战-", "1": "Dota-", "2": "IM-", "4": "自由匹配-", "3": "赛季模式-"}
users_chi = {0: "无", 1: "单", 2: "双", 3: "三", 4: "四", 5: "五"}

titles = ["杀", "MVP", "助", "躺", "灵", "僵"]

dg_titles = {"map_reserve2": "辅",
             "map_reserve4": "MVP",
             "map_reserve5": "杀",
             "map_reserve6": "助",
             "map_reserve7": "富",
             "map_reserve8": "SMVP"}


def get_ids(names):
    id_url = "https://users.09game.com/home/GetUserPub?user_name="
    ids = {}
    for name in names:
        url_name = urllib.parse.quote("\'" + name + "\'")
        response = requests.get(id_url + url_name)
        id = json.loads(response.text)["temp"][0]["user_id"]
        ids[name] = id
        response.close()
    print(ids)
    return ids


async def get_recent_data(id):
    recent_url = "https://score.09game.com/MOBA/BasicDataList?UserID={0}&GameTypeID=21&CurrentSeason=0&GameSource=-1&Time=-1&PageIndex=0&PageSize=6".format(
        str(id))
    response = requests.get(recent_url)
    content = json.loads(response.content)
    last_game = content["data"]["listEntity"][0]
    response.close()
    await asyncio.sleep(sleep_time)
    return last_game


async def get_dg_id(id):
    id_url = "https://score.09game.com/RPG/GameList?UserID={0}&GameTypeID=142&GameSource=-1&Type=2&Number=11".format(id)
    response = requests.get(id_url)
    content = json.loads(response.content)
    last_game = content["data"][0]
    response.close()
    await asyncio.sleep(sleep_time)
    return last_game


async def get_gids(id):
    """
    返回最近最多100场g_ids
    :param id:
    :return:
    """
    recent_most = "https://score.09game.com/moba/BasicDataList?UserID={0}&GameTypeID=21&CurrentSeason=0&GameSource=-1&Time=-1&PageIndex=0&PageSize=100".format(
        id)
    response = requests.get(recent_most)
    recent_data = json.loads(response.content)["data"]["listEntity"]
    response.close()
    g_ids = [x["g_id"] for x in recent_data]
    return g_ids


ids = get_ids(names=names)
ip = get_host_ip()
# print(get_recent_data(369818))

matcher = on_metaevent()

if ip == "10.10.10.8":
    first_time = int(time.time())
    group = 959822848
else:
    first_time = 1649837159
    # first_time = int(time.time())
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
        g_type = game_source[g_source]
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
        source_url = "https://cdn.09game.com/resources/game_skill/"
        omg_spend = int(data["time_length"]) // 60 + 1
        response = requests.get(id_url)
        detail = json.loads(response.content)
        response.close()
        # print(json.dumps(detail))
        users = 0
        for data in detail["data"]:
            if data["user_name"] in ids.keys():
                user_id = data["user_id"]
                kda = "{0}/{1}/{2}".format(data["kill_count"], data["killed_count"], data["assist_count"])
                hero_name, hero_level = data["hero_name"], data["hero_level"]
                guard = "近卫" if str(data["team_id"]) == "0" else "天灾"
                c_skills = [transfer_dId(x) for x in data["skills"].split(",")][4:6]
                title = data["title"]
                user_title = " " + get_title(title) + " "
                # print("c_skills:", c_skills)
                skill1 = MessageSegment.image(source_url + c_skills[0] + ".jpg")
                skill2 = MessageSegment.image(source_url + c_skills[1] + ".jpg")
                o_msg = o_msg + data[
                    "user_name"] + "-" + hero_name + "-" + str(
                    hero_level) + "级 " + guard + ":" + kda + user_title + "\n" + skill1 + skill2 + "\n"
                # print(omg_msg)
                users += 1
                team_id = data["team_id"]
                mc_gids = await get_gids(user_id)

        for data in detail["data"]:
            if data["user_name"] not in ids:
                if data["team_id"] == team_id and data["user_name"] not in ids:
                    street_ids = await get_gids(data["user_id"])
                    same_ids = list(set(mc_gids) & set(street_ids))
                    print("同局：".format(same_ids))
                    if len(same_ids) > 3:
                        users += 1
                people = "{0}排 ".format(users_chi[users])

        # 上面是人数
        omg_msg = "报：" + g_type + people + is_win + " {0}分钟\n".format(omg_spend) + o_msg
        print(omg_msg, len(omg_msg))
        # if len(omg_msg) > 1:
        if len(omg_msg) > 1 and ip == "10.10.10.8":
            print("send the omg msg")
            try:
                await bot.send_group_msg(group_id=group, message=omg_msg)
            except Exception as e:
                await bot.send_private_msg(user_id=281016636, message=str(omg_msg) + str(e))

    # else:
    #     print("OMG无")

    # DG模式
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
        dg_spend = int(dg_data["time_length"]) // 60 + 1
        response = requests.get(id_url)
        dg_detail = json.loads(response.content)
        response.close()
        for data in dg_detail["data"]:
            if data["user_name"] in ids.keys():
                # 图片
                user_title = ""
                extra_value = str(data["extra_value"])
                hero = re.search("英雄:.*?;", extra_value).group()[-5:-1]
                skill1, skill2 = re.search("额外技能1:.*?;", extra_value).group()[-5:-1], re.search("额外技能2:.*?;",
                                                                                                extra_value).group()[
                                                                                      -5:-1]
                hero_icon = MessageSegment.image("https://cdn.09game.com/resources/game_avator/" + hero + ".jpg")
                skill1_icon = MessageSegment.image("https://cdn.09game.com/resources/game_skill/" + skill1 + ".jpg")
                skill2_icon = MessageSegment.image("https://cdn.09game.com/resources/game_skill/" + skill2 + ".jpg")

                kda = re.match("击杀:\d+;死亡:\d+;助攻:\d+;", data["extra_value"]).group()
                for title in dg_titles.keys():
                    if data[title] != 0:
                        user_title += dg_titles[title]

                d_msg = d_msg + data["user_name"] + ":" + kda + " {} ".format(
                    user_title) + "\n" + hero_icon + skill1_icon + skill2_icon + "\n"

        dg_msg = "报：" + is_win + " {0}分钟\n".format(dg_spend) + d_msg
        print(dg_msg, len(dg_msg))
        if len(dg_msg) > 1 and ip == "10.10.10.8":
            print("send dg new msg")
            try:
                await bot.send_group_msg(group_id=group, message=dg_msg)
            except Exception as e:
                await bot.send_private_msg(user_id=281016636, message=str(dg_msg) + str(e))

# print(get_recent_data(369818))
# print(get_dg_id(369818))
