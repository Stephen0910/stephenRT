#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/1/29 16:14
# @Author   : StephenZ
# @Site     : 
# @File     : __init__.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2020>

from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot import on_message

msg_matcher = on_message()


async def send_private(bot: Bot, user_id, msg):
    await bot.send_private_msg(user_id=user_id, message=str(msg))


@msg_matcher.handle()
async def getMsg(bot: Bot, event: MessageEvent):
    msg = event
    print("msg:", msg)
    await send_private(bot, user_id=281016636, msg=msg)
