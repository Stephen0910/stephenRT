#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/2/24 17:46
# @Author   : StephenZ
# @Site     : 
# @File     : ban.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import datetime, time, re, requests, json
import stephenrt.privateCfg as cfg
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText

from nonebot.permission import SUPERUSER

config = cfg.config_content

env = "Prod"  # 根据环境读取配置
if env == "test":
    manager_base = config["manager_test"]
    user = config["manager_test_auth"]
    template_id = 9
else:
    manager_base = config["manager_prod"]
    user = config["manager_prod_auth"]
    template_id = 8

base_url = manager_base + "/login"
search_url = manager_base + "/badmintonCn/user_search_submit"
ban_url = manager_base + "/badmintonCn/user_search_forbidden"

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}


def search_user(user_id):
    payload = 'keyword={0}&searchWay=1'.format(user_id)
    try:
        session = requests.session()
        session.post(base_url, data=user, headers=headers)
        response = session.post(url=search_url, data=payload, headers=headers)
    except Exception as e:
        return str(e)
    return json.loads(response.content)


def get_msg(user_id):
    response = search_user(user_id)
    print("----------", response)
    if isinstance(response, str):
        return response
    if response["message"] != "Success":
        return response["message"]
    user_data = response["userList"][0]
    insert = ["number_user_id", "id", "name", "modify_name", "anti_addiction_name", "level", "totalPayMoney", "rank",
              "plat_form",
              "publish_channel", "client_version", "device_id", "forbidden_speak",
              "account_ban", "login_time"]
    msg = ""
    for key in insert:
        # msg = msg + key + "." * (maxlengh - len(key) + 3) + ":" + str(user_data[key]) + "\n"
        msg = msg + key + ":  " + str(user_data[key]) + "\n"
    return msg


def ban_user(id, ban_time, reason):
    """
    template_id暂时固定填8， 卖金币禁言3天
    :param user_id:
    :param ban_time: 天数
    :param reason:
    :return:
    """
    payload = {
        "userId": id,
        "forbidden_time": int(ban_time) * 1440,
        "template_id": template_id,
        "reason": reason
    }
    print("payload:", payload)
    print("ban_url:", ban_url)
    try:
        session = requests.session()
        session.post(base_url, data=user, headers=headers)
        response = session.post(url=ban_url, data=payload, headers=headers)
    except Exception as e:
        print(e)
        return str(e)
    return json.loads(response.content)


query = on_command("search", rule=to_me(), aliases={"find", "账号查询"}, priority=1)


@query.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg("user_id", args)  # 如果用户发送了参数则直接赋值


@query.got("user_id", prompt="【{0}环境】输入查询的用户数字id，如 128928".format(env))
async def handleuser(
        user_id: Message = Arg()
):
    # print("user_id:", user_id, type(user_id))
    if re.match("\d+\d$", str(user_id)):
        result = search_user(user_id)
        if isinstance(result, str) or result["status"] != 200:
            await query.finish("查询错误：" + result)
        else:
            msg = get_msg(user_id)
            await query.finish(msg)
    else:
        await query.finish("输入数字id错误，命令结束：" + user_id)


ban = on_command("ban", rule=to_me(), aliases={"禁言", "shut"}, priority=1, permission=SUPERUSER)


@ban.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg("user_id", args)  # 如果用户发送了参数则直接赋值


@ban.got("user_id", prompt="【{0}环境】输入禁言的用户数字id(如136246)".format(env))
@ban.got("ban_time", prompt="禁言时长(天)")
async def banUser(
        user_id: Message = Arg(),
        ban_time: int = ArgPlainText("ban_time")
):
    if re.match("\d+\d$", str(user_id)):
        result = search_user(user_id)
        print("result:", result)
        if isinstance(result, str) or result["status"] != 200:
            await query.finish("查询错误：" + result)
        if result["message"] != "Success":
            await query.finish(result["message"])
        user = result["userList"][0]
        keys = ["name", "modify_name", "level", "number_user_id", "rank"]
        infos = [user[key] for key in keys]

        key_infos = json.dumps(dict(zip(keys, infos)))
        await ban.send("请检查关键信息:" + str(key_infos))

        id = user["id"]
        now = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        if re.match("\d+", str(ban_time)):
            print(id, ban_time)
            result = ban_user(id=id, ban_time=ban_time, reason="广告" + now)
            await ban.finish("禁言结果：" + str(result))
    else:
        await ban.finish(user_id.template("输入数字id错误，命令结束：" + user_id))

# print(ban_user("60c06107e0b1c9c14bf303c081959296", 1, "test"))
# print(search_user(136246))
