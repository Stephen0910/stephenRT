#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/6/15 15:13
# @Author   : StephenZ
# @Site     : 
# @File     : season.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>
import requests
import json
import time
from nonebot import on_command
from nonebot.rule import to_me
from nonebot import get_bot
# from nonebot.matcher import Matcher
# from nonebot.adapters import Message
# from nonebot.params import Arg, CommandArg
from nonebot import on_metaevent
from nonebot.permission import SUPERUSER

season_url = "https://china.nba.cn/stats2/season/schedule.json?countryCode=CN&days=7&locale=zh_CN&tz=+8"
playof = "https://china.nba.cn/stats2/playoff/bracket.json?locale=zh_CN"
seasonData = "https://china.nba.cn/stats2/season/conferencestanding.json?locale=zh_CN"
team = "https://china.nba.cn/stats2/league/conferenceteamlist.json?locale=zh_CN"
team_player = "https://china.nba.cn/stats2/team/roster.json?locale=zh_CN&teamCode=hawks"
player = "https://china.nba.cn/stats2/player/stats.json?ds=career&locale=zh_CN&playerCode=stephen_curry"
player_of = "https://china.nba.cn/stats2/player/historicalstats.json?locale=zh_CN&playerCode=alex_acker"
kobe = "https://china.nba.cn/players/historical/#!/kobe_bryant"


async def transfer_time(timestamp):
    timestamp = int(timestamp)
    if timestamp > 3653284221:
        query_time = round(timestamp / 1000)
        nature = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(query_time))
    else:
        nature = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
    return nature


async def seasonInfo():
    with requests.get(season_url) as session:
        response = json.loads(session.text)
        dates = response["payload"]["dates"]
        for date in dates:
            games = date["games"]
            for game in games:
                profile = game["profile"]  # 基本信息
                boxscore = game["boxscore"]  # 比分信息
                urls = game["urls"]  # 腾讯直播地址
                broadcasters = game["broadcasters"]  # 其他直播地址
                homeTeam = game["homeTeam"]  # 主场信息
                awayTeam = game["awayTeam"]  # 客场信息

                nature = await transfer_time(profile["utcMillis"])
                # print("{0} 主场:{1} 客场:{2}".format(nature, homeTeam["profile"]["displayAbbr"], awayTeam["profile"]["displayAbbr"]))
        return dates


seasonInfo()

nbaInfo = on_command("nba", rule=to_me(), aliases={"篮球", "NBA"}, priority=1, permission=SUPERUSER)


@nbaInfo.handle()
async def get_seasonInfo():
    msg = "NBA近7日赛程：\n"
    dates = await seasonInfo()
    for date in dates:
        games = date["games"]
        for game in games:
            profile = game["profile"]  # 基本信息
            boxscore = game["boxscore"]  # 比分信息
            urls = game["urls"]  # 腾讯直播地址
            broadcasters = game["broadcasters"]  # 其他直播地址
            homeTeam = game["homeTeam"]  # 主场信息
            awayTeam = game["awayTeam"]  # 客场信息
            nature = await transfer_time(profile["utcMillis"])
            msg += "⬤  {0} 【主场】{1} vs {2}\n".format(nature, homeTeam["profile"]["displayAbbr"],
                                                   awayTeam["profile"]["displayAbbr"])
    await nbaInfo.finish(msg)


nbalive = on_command("nbalive", rule=to_me(), aliases={"实时", "比分"}, priority=1, permission=SUPERUSER)


@nbalive.handle()
async def get_seasonInfo():
    scores = []
    dates = await seasonInfo()
    for date in dates:
        games = date["games"]
        for game in games:
            profile = game["profile"]  # 基本信息
            boxscore = game["boxscore"]  # 比分信息
            urls = game["urls"]  # 腾讯直播地址
            broadcasters = game["broadcasters"]  # 其他直播地址
            homeTeam = game["homeTeam"]  # 主场信息
            awayTeam = game["awayTeam"]  # 客场信息
            nature = await transfer_time(profile["utcMillis"])
            # print(boxscore["status"])
            if boxscore["status"] == "0":
                scores.append("⬤  {0} vs {1} {5}  实时比分 {2}:{3} 比赛时间 {4}".format(homeTeam["profile"]["displayAbbr"],
                                                                                awayTeam["profile"]["displayAbbr"],
                                                                                boxscore["homeScore"],
                                                                                boxscore["awayScore"],
                                                                                boxscore["gameLength"],
                                                                                boxscore["statusDesc"]))
    print(scores)
    if len(scores) == 0:
        await nbaInfo.finish("当前无比赛")
    else:
        msg = "NBA实时比分：\n"
        for score in scores:
            msg += score + "\n"
        await nbaInfo.finish(msg)


noti = on_metaevent()
trigger = 1
livelist = []
first_time = int(time.time())


@noti.handle()
async def live_noti():
    global trigger
    if trigger % 5 == 0:
        bot = get_bot()
        dates = await seasonInfo()
        msg = "NBA实况信息:\n"
        for date in dates:
            games = date["games"]
            for game in games:
                profile = game["profile"]  # 基本信息
                boxscore = game["boxscore"]  # 比分信息
                urls = game["urls"]  # 腾讯直播地址
                broadcasters = game["broadcasters"]  # 其他直播地址
                homeTeam = game["homeTeam"]  # 主场信息
                awayTeam = game["awayTeam"]  # 客场信息
                nature = await transfer_time(profile["utcMillis"])
                gameId = profile["gameId"]
                status = str(gameId) + boxscore["status"]
                if boxscore["status"] == "1":
                    print("{0}未开始".format(gameId))
                    continue
                elif boxscore["status"] != "1" and status not in livelist and int(
                        profile["utcMillis"]) > first_time * 1000:
                    livelist.append(status)
                    msg += "⬤  {0} vs {1} {5}  实时比分 {2}:{3} 比赛时间 {4}".format(homeTeam["profile"]["displayAbbr"],
                                                                             awayTeam["profile"]["displayAbbr"],
                                                                             boxscore["homeScore"],
                                                                             boxscore["awayScore"],
                                                                             boxscore["gameLength"],
                                                                             boxscore["statusDesc"])

                    await bot.send_private_msg(user_id=281016636, message=msg)
                else:
                    print("已经播报过了")


    else:
        print("nba trigger:{0}".format(trigger))
    trigger += 1
