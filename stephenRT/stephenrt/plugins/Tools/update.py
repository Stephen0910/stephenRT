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
import os, subprocess

update = on_command("update", rule=to_me(), aliases={"更新", "selfupdate"}, priority=1, permission=SUPERUSER)


async def run_silently(cmd):
    with os.popen(cmd) as fp:
        bf = fp._stream.buffer.read()
    try:
        return bf.decode().strip()
    except UnicodeDecodeError:
        return bf.decode('gbk').strip()

async def run_cmd(cmd):
    with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8") as f:
        data = f.stdout.read()
    return data


prompt = "请输入你要执行的指令\nq放弃"


@update.got("cmd", prompt=prompt)
async def handleuser(
        cmd: str = ArgPlainText("cmd")
):
    print("cmd:", cmd)
    if cmd == "q":
        await update.finish("放弃执行指令，会话结束")
    elif cmd == "update":
        # run_cmd("cd /home/ttg/Tools/project/robot/stephenRT/stephenRT")
        git_status = await run_cmd("git pull")
        await update.send("git更新结果：\n" + git_status)
        ret = await run_silently("sh /home/ttg/Tools/project/robot/bot_restart.sh")
        # ret = run_cmd("sh /home/ttg/Tools/project/robot/bot_restart.sh")
        await update.finish("执行结果：\n" + ret)
    else:
        ret = await run_cmd(cmd)
        await update.finish(str(ret))

