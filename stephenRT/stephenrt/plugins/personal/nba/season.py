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


season_headers = {
  'authority': 'china.nba.cn',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
  'cookie': 'i18next=zh_CN; locale=zh_CN; AMCVS_248F210755B762187F000101%40AdobeOrg=1; countryCode=CN; s_cc=true; privacyV2=true; s_sq=%5B%5BB%5D%5D; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22181662f9fd3e-01dbf86a314dbf9-26021b51-2073600-181662f9fd4ca%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgxNjYyZjlmZDNlLTAxZGJmODZhMzE0ZGJmOS0yNjAyMWI1MS0yMDczNjAwLTE4MTY2MmY5ZmQ0Y2EifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22181662f9fd3e-01dbf86a314dbf9-26021b51-2073600-181662f9fd4ca%22%7D; AMCV_248F210755B762187F000101%40AdobeOrg=-1712354808%7CMCIDTS%7C19161%7CMCMID%7C64061681013499296691299490953705543050%7CMCAAMLH-1656042813%7C11%7CMCAAMB-1656042813%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1655445213s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.3.0; tp=2629; s_ppv=cn%253Astats%253Aplayers%253Astephen_curry%253Astats%2C36%2C36%2C937; s_gpv=no%20value; nbachina=MTY1NTQ0NDc2M3xrYXo5MFBnakpuS3N3NEdhTUVNenczTU9WRERoUnhNSVdua1B4d3dZaDVKNkJvTlQzTXprUm9LSTQ2NXFnYUJlNUNRYUNaY2V6TEd0eFFjVVB5aElxRFNvRFFONVJSR1l88A287OCivnKcLqlxhL4pij-LAmD0IF3bIITY7jica78=',
  'if-none-match': '"2842-49b34a4123c3cff0131190f2a5d396d4dba099a9"',
  'referer': 'https://china.nba.cn/schedule/',
  'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
}

async def transfer_time(timestamp):
    timestamp = int(timestamp)
    if timestamp > 3653284221:
        query_time = round(timestamp / 1000)
        nature = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(query_time))
    else:
        nature = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
    return nature


async def seasonInfo():
    with requests.get(season_url, headers = season_headers) as session:
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


async def now_score(gameId):
    url = "https://china.nba.cn/stats2/game/playbyplay.json?gameId={0}&locale=zh_CN&period=2".format(gameId)
    with requests.get(url) as session:
        response = json.loads(session.text)
        boxscore = response["payload"]["boxscore"]
        return boxscore


nbaInfo = on_command("nba", rule=to_me(), aliases={"篮球", "NBA"}, priority=1)


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
            status = boxscore["statusDesc"] if boxscore["statusDesc"] != None else "未开始"
            msg += "⬤  {0} (主场){1} vs {2}  【{3}】\n".format(nature, homeTeam["profile"]["displayAbbr"],
                                                    awayTeam["profile"]["displayAbbr"], status)
    await nbaInfo.finish(msg)


nbalive = on_command("nbalive", rule=to_me(), aliases={"实时", "比分", "live"}, priority=1)


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
            gameId = profile["gameId"]
            nature = await transfer_time(profile["utcMillis"])
            # print(boxscore["status"])
            if boxscore["status"] == "2":
                boxscore = await now_score(gameId)
                scores.append("⬤  (主){0} vs {1}  ({5} {4})\n 比分：{2}:{3}".format(homeTeam["profile"]["displayAbbr"],
                                                                               awayTeam["profile"]["displayAbbr"],
                                                                               boxscore["homeScore"],
                                                                               boxscore["awayScore"],
                                                                               boxscore["periodClock"],
                                                                               boxscore["statusDesc"]))

                # scores.append("⬤  {0} vs {1} {5} 剩余时间 {4}\n {2}:{3}".format(homeTeam["profile"]["displayAbbr"],
                #                                                                 awayTeam["profile"]["displayAbbr"],
                #                                                                 boxscore["homeScore"],
                #                                                                 boxscore["awayScore"],
                #                                                                 boxscore["periodClock"],
                #                                                                 boxscore["statusDesc"]))
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
                status = str(gameId) + ":" +boxscore["status"]
                if boxscore["status"] == "1":
                    print("{0}未开始".format(gameId))
                    continue
                elif boxscore["status"] != "1" and status not in livelist and int(
                        profile["utcMillis"]) > first_time * 1000:
                    livelist.append(status)
                    msg += ("⬤  (主){0} vs {1}  ({5} {4})\n 比分：{2}:{3}".format(homeTeam["profile"]["displayAbbr"],
                                                                             awayTeam["profile"]["displayAbbr"],
                                                                             boxscore["homeScore"],
                                                                             boxscore["awayScore"],
                                                                             boxscore["periodClock"],
                                                                             boxscore["statusDesc"]))

                    await bot.send_private_msg(user_id=281016636, message=msg)
                else:
                    print("不播报:", status)


    else:
        print("nba trigger:{0}".format(trigger))
    trigger += 1
