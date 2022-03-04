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


import time, re, requests, json, logging, logzero
import stephenrt.privateCfg as cfg
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.params import Depends
from nonebot.params import ArgStr, LastReceived
import asyncio
from logzero import logger

logzero.loglevel(logging.DEBUG)
config = cfg.config_content

headers = {
    "Content-Type": "application/json"
}


async def search_user(search_info, env):
    search_info = str(search_info)
    if env == "test":
        logger.debug("search_user: 测试环境")
        manager_base = config["manager_test"]
        user = config["manager_test_auth"]
    else:
        logger.debug("search_user: 正式环境")
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
    try:
        with requests.session() as session:
            session.post(url=base_url, json=user, headers=headers)
            response = session.post(url=search_url, json=payload, headers=headers)
    except Exception as e:
        return str(e)
    result = json.loads(response.content)
    logger.debug(search_id)
    logger.debug("result:" + json.dumps(result))
    return result


def transferMsg(response, long=True):
    try:
        status, userList, message = response["status"], response["userList"], response["message"]
    except Exception:
        error_msg = "解析响应错误:" + str(response)
        logger.debug(error_msg)
        return error_msg
    if status != 200 or message != "Success":
        return str(message)
    else:
        # print("------------------", len(userList))
        # logger.debug("userList:", userList)
        # logger.debug(len(userList))
        msg = "查询有{0}条数据\n".format(len(userList))
        if len(userList) > 6:
            userList = userList[:5]
        if len(userList) < 2:
            key_words = ["number_user_id", "id", "name", "modify_name", "anti_addiction_name", "level",
                         "rank", "totalPayMoney",
                         "plat_form",
                         "publish_channel", "client_version", "forbidden_speak",
                         "account_ban","gold_num", "diamond_num", "login_time"]
            msg = ""
        else:
            key_words = ["number_user_id", "name", "modify_name","rank", "level"]

        # logger.debug("key_words:", key_words)
        # msg = "-" * 20 + "\n"

        for user in userList:
            middle_dic = {}
            for key in key_words:
                if user[key] != "" and user[key] is not None:
                    middle_dic[key] = user[key]
                    msg = msg + key + ":  " + str(user[key]) + "\n"
            msg += "-" * 20 + "\n"
        logger.debug(msg)
        logger.debug(type(msg))
        return msg


def get_template(env):
    """
    获取模板
    :param env:
    :return:
    """
    payload = {}
    if env == "test":
        logger.debug("测试环境")
        manager_base = config["manager_test"]
        user = config["manager_test_auth"]
    else:
        logger.debug("正式环境")
        manager_base = config["manager_prod"]
        user = config["manager_prod_auth"]
    base_url = manager_base + "/login"
    template_url = manager_base + "/badmintonCn/user_search_get_template"
    try:
        session = requests.session()
        session.post(base_url, json=user, headers=headers)
        response = session.post(url=template_url, json=payload, headers=headers)
    except Exception as e:
        return str(e)
    result = json.loads(response.content)
    return result


async def ban_user(id, ban_time, reason, env):
    """
    template_id
    :param user_id:
    :param ban_time: 天数
    :param reason:
    :return:
    """
    # env = "test"
    if env == "test":
        logger.debug("测试环境")
        manager_base = config["manager_test"]
        user = config["manager_test_auth"]
    else:
        logger.debug("正式环境")
        manager_base = config["manager_prod"]
        user = config["manager_prod_auth"]

    base_url = manager_base + "/login"
    ban_url = manager_base + "/badmintonCn/user_search_forbidden"
    logger.error(ban_time)
    if ban_time == "1" or ban_time == "0":
        template_id = 3  # 24h
    elif ban_time == "7":
        template_id = 2
    elif ban_time == "90":
        template_id = 1
    elif ban_time == "3":
        template_id = 8
    else:
        template_id = ""
    if env == "test":
        template_id = 9
    payload = {
        "userId": id,
        "forbidden_time": str(int(ban_time) * 1440),
        "template_id": template_id,
        "reason": reason
    }
    try:
        with requests.session() as session:
            session.post(base_url, json=user, headers=headers)
            response = session.post(url=ban_url, json=payload, headers=headers)
    except Exception as e:
        logger.debug(e)
        return str(e)
    # logger.info(json.dumps(user))

    # logger.info(json.dumps(payload))

    # logger.info(response.content)
    return str(response.content).encode("utf-8")


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
    # response = find_user(search_info, env)
    response = await search_user(search_info, env)
    msg = transferMsg(response, long=True)
    logger.debug("msg:", msg)
    # await find_test.send("(使用{0}查询)".format(search_ways[search_id]))
    await find_test.finish(message=msg)


"""正式服find"""

find_prod = on_command("find", rule=to_me(), aliases={"searcht", "findp"}, priority=1)


@find_prod.handle()
async def prod_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg("search_info", args)  # 如果用户发送了参数则直接赋值


@find_prod.got("search_info", prompt="输入要查询的ID或名字或id")
async def hand_find(
        search_info: Message = Arg()
):
    env = "prod"
    search_info = str(search_info)
    response = await search_user(str(search_info), env)
    msg = transferMsg(response, long=True)
    # await find_test.send("(使用{0}查询)".format(search_ways[search_id]))
    await find_test.finish(message=msg)


"""禁言-仅正式服"""

ban = on_command("ban", rule=to_me(), aliases={"jy", "shut"}, priority=1, permission=SUPERUSER)


@ban.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg("user_id", args)  # 如果用户发送了参数则直接赋值


temps = "禁言90日处罚/禁言7日处罚/禁言1日处罚/禁言3日金币处罚/q放弃 "


@ban.got("user_id", prompt="输入禁言的用户数字id(如136246)")
@ban.got("ban_time", prompt="禁言天数: {0}".format(temps))
async def banUser(
        user_id: str = ArgPlainText("user_id"),
        ban_time: str = ArgPlainText("ban_time")
):
    env = "prod"
    if re.match("\d+\d$", user_id):
        result = await search_user(user_id, env)
        print("result:", result)
        if isinstance(result, str) or result["status"] != 200:
            await ban.finish("查询错误：" + result)
        if result["message"] != "Success":
            await ban.finish(result["message"])
        user = result["userList"][0]
        # keys = ["name", "modify_name", "level", "number_user_id", "rank"]
        # infos = [user[key] for key in keys]

        # key_infos = json.dumps(dict(zip(keys, infos)))
        # await ban.send("请检查关键信息:" + str(key_infos))

        id = user["id"]
        now = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        if ban_time == "q":
            await ban.finish("放弃禁言，会话结束")
        if re.match("\d+", ban_time):
            logger.debug(id)
            logger.debug(ban_time)
            result = await ban_user(id=id, ban_time=str(ban_time), reason="QQ禁" + now, env=env)
            await ban.finish("禁言结果：" + str(result))
    else:
        await ban.finish(user_id.template("输入数字id错误，命令结束：" + user_id))
