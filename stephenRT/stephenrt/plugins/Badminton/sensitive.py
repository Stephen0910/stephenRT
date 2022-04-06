#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/2/15 16:47
# @Author   : StephenZ
# @Site     : 
# @File     : sensitive.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Event
from nonebot import on_message
import os, sys, datetime
import jieba
import re
import asyncpg
import socket

sys.path.append("../../")
import stephenrt.privateCfg as cfg

config = cfg.config_content
report_to = config["user_id"]
user_id = config["user_id"]


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


if get_host_ip() == "10.10.10.8":
    group_id = config["group_id_test"]
    check_gpName = "决战羽毛球"
else:
    group_id = config["group_id_test"]
    check_gpName = "Robot"

print(group_id, check_gpName)


def get_sens():
    """
    获取屏蔽词
    :return:
    """
    rootdir = os.path.join(os.getcwd(), "stephenrt", "plugins", "Badminton", "mgc")
    # print("rootdir:", rootdir)
    sens_words = []
    for root, dirs, files in os.walk(rootdir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                sens_words += [line.strip() for line in open(file_path, 'r', encoding='utf-8').readlines()]
            except Exception as e:
                print(e)
                sens_words += [line.strip() for line in open(file_path, 'r', encoding='gbk').readlines()]

    return [sens for sens in sens_words if sens != ""]  # 避免有空


def get_white():
    white_path = os.path.join(os.getcwd(), "stephenrt", "plugins", "Badminton", "white.txt")
    return white_path


async def group_info(bot: Bot, groupId):
    """
    获取群信息，可以获取群名
    :param bot:
    :param groupId:
    :return:
    """
    groupInfo = await bot.get_group_info(group_id=groupId)
    print(groupInfo)
    return groupInfo


async def send_private(bot: Bot, user_id, msg):
    """
    发送私聊信息
    :param bot:
    :param user_id:
    :param msg:
    :return:
    """
    await bot.send_private_msg(user_id=user_id, message=str(msg))


async def delete_msg(bot: Bot, msgid):
    """
    撤回消息
    :param bot:
    :param msgid:
    :return:
    """
    try:
        await bot.delete_msg(message_id=msgid)
        print("撤回成功")
    except Exception as e:
        result = "撤回失败：{0}".format(e)
        await send_private(bot, user_id=report_to, msg=result)


async def save_dirty(sql):
    conn = await asyncpg.connect(user=config["user"], password=config["password"], database=config["database"],
                         host=config["host"])
    await conn.execute(sql)
    await conn.close()


msg_matcher = on_message()

sens = get_sens()
# print("sens:", sens)
white = get_white()


@msg_matcher.handle()
async def checkMessage(bot: Bot, event: GroupMessageEvent):
    msg = event
    or_msg = str(msg.message).replace("\n", "").replace("\r", "").replace(" ", "")  # 去掉空格换行
    # print("debug:", or_msg)
    jieba_msg = re.sub('\[CQ:\w+,.+?\]', "", or_msg)  # 图片等信息过滤
    sen_text = re.compile(u'[\u4E00-\u9FA5|\s\w]').findall(jieba_msg)  # 去掉所有标点符号
    pure_msg = "".join(sen_text)
    print("pure_msg:", pure_msg)
    jieba.load_userdict(sens)  # 优先拆分敏感词
    jieba.load_userdict(get_white())  # 白名单词
    content = jieba.lcut(pure_msg, cut_all=False)  # 避免误报，使用分词
    print("分词结果:", content)

    for word in sens:  # word: 屏蔽词库  content: message的结巴分词列表
        if word in content:
            print("word:", word, len(word))
            groupInfo = await group_info(bot, msg.group_id)
            group_name = groupInfo["group_name"]
            sender = msg.sender
            sender_id = sender.user_id
            # if "羽毛球" in group_name:
            message_id = msg.message_id
            if sender.card != "":
                name = sender.card
            else:
                name = sender.nickname
            if check_gpName in group_name:  # 这里要做权限隔离  不要所有都检测
                print("符合群规则")
                dateArray = datetime.datetime.utcfromtimestamp(msg.time + 8 * 3600)  # 时区加8)
                msg_time = dateArray.strftime("%Y-%m-%d %H:%M:%S")
                sql = """
                INSERT INTO "public"."dirty"("timestamp", "group_id", "group_name", "user_id", "user_name", "message", "key") VALUES ('{0}', {1}, '{2}', {3}, '{4}', '{5}', '{6}');
                """.format(msg_time, group_id, group_name, sender_id, name, or_msg, word)
                await save_dirty(sql)
                send_message = "{0}|{1} 发送敏感内容:【{2}】\n(敏感词:{3})".format(group_name, name, or_msg, word)
                # await send_private(bot, user_id=report_to,
                #                    msg="{0}|{1} 发送敏感内容:【{2}】\n(敏感词:{3})".format(group_name, name, or_msg, word))
                try:
                    await bot.send_group_msg(group_id=group_id, message=send_message)
                except Exception as e:
                    await bot.send_private_msg(user_id=user_id, message=str(e))
                    await bot.send_private_msg(user_id=user_id, message=str(send_message))
                # finally:
                #     await delete_msg(bot, message_id) # 暂不启用
                break  # 重复的脏字会导致发送两次修复

    # for word in content:
    #     if word in sens:
    #         print("检测到：", word)
    #         return
