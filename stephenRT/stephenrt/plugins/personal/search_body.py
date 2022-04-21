#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/4/14 14:43
# @Author   : StephenZ
# @Site     : 
# @File     : search_body.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import MessageEvent
import urllib, requests, json
from .dGame import get_rPic
from nonebot.adapters.onebot.v11.message import MessageSegment
from nonebot.params import Depends

players = [281016636, 659738900, 158709003, 726408753]


def get_id(name):
    id_url = "https://users.09game.com/home/GetUserPub?user_name="
    ids = {}
    url_name = urllib.parse.quote("\'" + name + "\'")
    response = requests.get(id_url + url_name)
    id = json.loads(response.text)["temp"][0]["user_id"]
    ids[name] = id
    response.close()
    return id


dGame = on_command("dota", rule=to_me(), aliases={"dota1", "09"}, priority=1)


@dGame.handle()
async def msg_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  #
    if plain_text:
        matcher.set_arg("user_name", args)  # 如果用户发送了参数则直接赋值


# 查询类
async def search_user_info(name):
    # id
    print("调用查询")
    try:
        user_id = get_id(name)
    except:
        return "查无此人"
    print("user_id", user_id)
    # return user_id
    msg = "⬤  id: {0}\n".format(user_id)
    # 胜率
    s = requests.get(url="https://score.09game.com/Ordinary/SeasonSummary?UserID={0}&GameTypeID=21".format(user_id))
    user_data = json.loads(s.content)["data"]
    s.close()
    if user_data["total"] == []:
        return "无OMG数据"
    elif user_data["season"] == []:
        season_data = "赛季数据无\n"
    else:
        season_total = user_data["season"][0]["total_times"]
        season_win = user_data["season"][0]["total_win"]
        if season_total == 0:
            season_data = "赛季0场"
        else:
            season_data = "赛季{0}场".format(season_total) + ":{:.0%}\n".format(season_win / season_total)
    all_total = user_data["total"][0]["total_times"]
    all_win = user_data["total"][0]["total_win"]
    if all_total == 0:
        total_data = "⬤  共0场"
    else:
        total_data = "⬤  共{0}场".format(all_total) + ":{:.0%}  ".format(all_win / all_total)

    msg = msg + total_data + season_data

    s = requests.get("https://score.09game.com/MOBA/GameDataStatistics?UserID={0}&GameTypeID=21".format(user_id))
    person = json.loads(s.content)["data"]
    s.close()
    hours = person["total"][0]["total_timelen"] // 3600
    total_triple_kill = person["total"][0]["total_triple_kill"]
    person_info = "⬤  时长:{0}小时, 三杀:{1}次\n".format(hours, total_triple_kill)

    msg += person_info

    s = requests.get("https://score.09game.com/MOBA/UserRanking?gameTypeId=21&UserID={0}".format(user_id))
    rank = json.loads(s.content)

    s.close()
    if rank["data"] == []:
        return msg
    rank_info = "⬤  积分:{0}, 排名:{2},竞技场积分:{1}".format(rank["data"][0]["score"], rank["data"][0]["arena_score"],
                                                        rank["data"][0]["rank_number"])

    msg += rank_info

    return msg


@dGame.got("user_name", prompt="输入要查询的名字")
async def user_search(
        user_name: str = ArgPlainText("user_name")
):
    user_info = await search_user_info(user_name)
    await dGame.finish(str(user_info))




# pic

async def depend(event: MessageEvent): # 2.编写依赖函数
    return {"uid": event.get_user_id(), "nickname": event.sender.nickname}

picture = on_command("setu", rule=to_me(), aliases={"图", "pic"}, priority=1)

@picture.handle()
async def get_pic(x: dict = Depends(depend)):
    print("pId:", x["uid"])
    if int(x["uid"]) in players:
        pic_url = await get_rPic()
        image = MessageSegment.image(pic_url)
        await picture.finish(image)
    else:
        print("无法操作")
        await picture.finish()