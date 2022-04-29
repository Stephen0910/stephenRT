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
from nonebot.params import Arg, CommandArg, ArgPlainText
from nonebot.permission import SUPERUSER
import os

update = on_command("update", rule=to_me(), aliases={"更新", "selfupdate"}, priority=1, permission=SUPERUSER)


def run_silently(cmd):
    with os.popen(cmd) as fp:
        bf = fp._stream.buffer.read()
    try:
        return bf.decode().strip()
    except UnicodeDecodeError:
        return bf.decode('gbk').strip()


prompt = "请输入你要执行的指令\nq放弃"


@update.got("cmd", prompt=prompt)
async def handleuser(
        cmd: str = ArgPlainText("cmd")
):
    print("cmd:", cmd)
    if cmd == "q":
        await update.finish("放弃执行指令，会话结束")
    elif cmd == "update":
        run_silently("cd /home/ttg/Tools/project/robot/stephenRT/stephenRT")
        git_status = run_silently("git pull")
        await update.send("git更新结果：\n" + git_status)
        # run_silently("cd /home/ttg/Tools/project/robot")
        ret = run_silently("sh /home/ttg/Tools/project/robot/bot_restart.sh")
        await update.finish("执行结果：\n" + ret)
    else:
        ret = run_silently(cmd)
        await update.finish(str(ret))

