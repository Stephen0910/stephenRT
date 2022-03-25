#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/3/25 16:08
# @Author   : StephenZ
# @Site     : 
# @File     : update.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>


import time, re, datetime
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg
from nonebot.permission import SUPERUSER
import os

update = on_command("update", rule=to_me(), aliases={"更新", "selfupdate"}, priority=1, permission=SUPERUSER)


@update.handle()
async def handleuser(
):
    cmd = "ifconfig"
    po = os.popen(cmd)
    msg = po.buffer.read().decode('utf-8')

    print("msg:", msg)
    # success = str(os.popen("./bot_restart.sh").read()).encode("utf-8")
    # await update.finish(str(success))
    await update.finish("完")

