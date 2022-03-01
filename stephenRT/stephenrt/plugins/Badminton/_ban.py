#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/2/28 15:07
# @Author   : StephenZ
# @Site     : 
# @File     : _ban.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>


import time, re, requests, json
import stephenrt.privateCfg as cfg
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.params import Depends
from nonebot.params import ArgStr

config = cfg.config_content

# env = "test"  # 根据环境读取配置
# if env == "test":
#     manager_base = config["manager_test"]
#     user = config["manager_test_auth"]
#     template_id = 9
# else:
#     manager_base = config["manager_prod"]
#     user = config["manager_prod_auth"]
#     template_id = 8
#
# base_url = manager_base + "/login"
# search_url = manager_base + "/badmintonCn/user_search_submit"
# ban_url = manager_base + "/badmintonCn/user_search_forbidden"

headers = {
    "Content-Type": "application/json"
}


def find_user(search_info, env):
    # payload = 'keyword={0}&searchWay={1}'.format(user_id, searchWay)
    search_info = str(search_info)
    if env == "test":
        print("测试环境")
        manager_base = config["manager_test"]
        user = config["manager_test_auth"]
    else:
        print("正式环境")
        manager_base = config["manager_prod"]
        user = config["manager_prod_auth"]

    base_url = manager_base + "/login"
    search_url = manager_base + "/badmintonCn/user_search_submit"
    if re.match("\d+$", search_info):
        search_id = 1
    elif re.match("^[a-zA-Z0-9]+$", str(search_info)) and len(search_info) > 15:
        search_id = 2
    else:
        search_id = 3
    payload = {"keyword": search_info, "searchWay": search_id}
    print("payload:", payload)
    try:
        session = requests.session()
        session.post(base_url, json=user, headers=headers)
        response = session.post(url=search_url, json=payload, headers=headers)
    except Exception as e:
        return str(e)
    result = json.loads(response.content)
    return result


def transferMsg(response, long=True):
    print("res:\n", response)
    print(type(response))
    try:
        status, userList, message = response["status"], response["userList"], response["message"]
    except Exception as e:
        print("e:", str(e))
        return str(e)
    if status != 200 or message != "Success":
        return str(message)
    else:
        key_words = ["number_user_id", "id", "name", "modify_name", "anti_addiction_name", "level",
                     "rank",
                     "plat_form",
                     "publish_channel", "client_version", "forbidden_speak",
                     "account_ban", "login_time"]
        users_words = ["number_user_id", "name", "modify_name"]
        msg = ""
        if len(userList) > 1 or long == False:
            msg += "共查询获得数据：{0}条\n".format(len(userList))
            for user in userList:
                # user_data = [user[x] for x in key_words]
                for key in users_words:
                    msg = msg + key + ":  " + str(user[key]) + "\n"
        else:
            users = userList[0]
            for key in key_words:
                msg = msg + key + ":  " + str(users[key]) + "\n"
        return msg


"""测试服findt"""

find_test = on_command("findt", rule=to_me(), aliases={"searcht"}, priority=1)


@find_test.handle()
async def test_recieve(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg("search_info", args)  # 如果用户发送了参数则直接赋值


@find_test.got("search_info", prompt="输入要查询的信息:")
async def hand_findt(
        search_info: Message = Arg()
):
    env = "test"
    search_info = str(search_info)
    search_ways = ["无", "数字ID", "用户ID", "昵称"]

    response = find_user(search_info, env)
    print("keyword:", search_info)

    msg = transferMsg(response)
    print("msg:", msg)
    # await find_test.send("(使用{0}查询)".format(search_ways[search_id]))
    await find_test.finish(message=msg)


"""正式服find"""

find_prod = on_command("find", rule=to_me(), aliases={"searcht", "findp"}, priority=1)


@find_prod.handle()
async def prod_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg("search_info", args)  # 如果用户发送了参数则直接赋值


@find_prod.got("search_info", prompt="输入要查询的信息:")
async def hand_find(
        search_info: Message = Arg()
):
    env = "prod"
    search_info = str(search_info)
    response = find_user(str(search_info), env)
    print("keyword:", search_info)

    msg = transferMsg(response)
    print("msg:", msg)
    # await find_test.send("(使用{0}查询)".format(search_ways[search_id]))
    await find_test.finish(message=msg)


"""禁言-仅正式服"""

shut = on_command("jy", rule=to_me(), aliases={"ban", "shut"}, priority=1, permission=SUPERUSER)


@shut.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg("user_id", args)  # 如果用户发送了参数则直接赋值
        # if re.match("\d+", str(args)):
        #     await shut.finish("直接结束了")


# 依赖注入 获取用户名和id
async def depend(event: MessageEvent):  # 2.编写依赖函数
    return {"uid": event.get_user_id(), "nickname": event.sender.nickname}


@shut.got("user_id", prompt="【正式环境】输入禁言的用户数字id(如128928)")
async def banUser(
        user_id: Message = Arg(),

):
    number_user_id = str(user_id)
    if re.match("\d+$", number_user_id):
        user_info = find_user(user_id, env="prod")
        user_info = transferMsg(user_info, long=False)
        checkmsg = "请检查关键信息：\n" + user_info + "\n"
        print("checkmsg:", checkmsg)

        @shut.got("ban_time", prompt="{0}禁言时长(天)".format(checkmsg))
        async def forbidden(
                ban_time: str = ArgPlainText()
        ):
            await shut.finish(str(ban_time))
    else:
        await shut.finish("会话结束，数字ID输入错误: {0}\n".format(number_user_id))

        # await shut.finish(str(x))


"""------------------------"""
# def check_pw(user_id, pw):
#     print(user_id, pw)
#     pass
#
#
# users = [1, 2, 3]
# login = on_command("login", rule=to_me(), aliases={"lg"}, priority=1, permission=SUPERUSER)
#
#
# @login.got("user", prompt="用户id")
# @login.got("password", prompt="密码")
# async def func1(
#         user: str = ArgStr("user"),
#         password: str = ArgStr("password")
# ):
#     if user not in users:
#         await login.finish("没有账号")
#     else:
#         # 登陆流程pass
#         check_pw(user, password)
#         await login.finish("登陆ok")
