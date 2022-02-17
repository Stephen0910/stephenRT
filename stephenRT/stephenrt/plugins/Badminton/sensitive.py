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
import os, sys
import jieba
import re

sys.path.append("../../")
import stephenrt.privateCfg as cfg

config = cfg.config_content
report_to = config["user_id"]


def get_sens():
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
    try:
        await bot.delete_msg(message_id=msgid)
        print("撤回成功")
    except Exception as e:
        result = "撤回失败：{0}".format(e)
        await send_private(bot, user_id=report_to, msg=result)


msg_matcher = on_message()

sens = get_sens()
# print(sens)
# print(len(sens))


@msg_matcher.handle()
async def checkMessage(bot: Bot, event: GroupMessageEvent):
    msg = event
    or_msg = str(msg.message)
    print("debug:", or_msg)
    jieba_msg = re.sub('\[CQ:\w+,.+?\]', "", or_msg)
    content = list(jieba.cut(jieba_msg, cut_all=False))  # 避免误报，使用分词
    print("分词content:", content)

    for word in sens:
        if word in content:  # cq误报ma
            # print("word:", word, len(word))
            # print("content:", content, len(content))
            groupInfo = await group_info(bot, msg.group_id)
            group_name = groupInfo["group_name"]
            sender = msg.sender
            # if "羽毛球" in group_name:
            message_id = msg.message_id
            if sender.card != "":
                name = sender.card
            else:
                name = sender.nickname
            # if "羽毛球" in group_name: # 这里要做权限隔离  不要所有都检测
            await send_private(bot, user_id=report_to,
                               msg="{0}|{1} 发送敏感内容:【{2}】\n(敏感词:{3})".format(group_name, name, or_msg, word))
            # await delete_msg(bot, message_id) # 暂不启用
            break  # 重复的脏字会导致发送两次修复
