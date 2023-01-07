#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/1/6 11:35
# @Author   : StephenZ
# @Site     : 
# @File     : aichat.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2023
# @Licence  :     <@2022>

import openai
import time, re, datetime
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg
from nonebot.permission import SUPERUSER
import stephenrt.privateCfg as cfg

config = cfg.config_content

openai.api_key = config["openai"]

print("chatgpt 加载成功")

chatgpt = on_command("op", rule=to_me(), aliases={"cg", "ai", "请问", "你知道", "知道", "知不知道", "问"}, priority=1, permission=SUPERUSER)


model = "text-davinci-003"

async def chat2opt(prompt):
    completions = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0,
    )

    message = completions.choices[0].text
    return message


@chatgpt.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg("question", args)  # 如果用户发送了参数则直接赋值


@chatgpt.got("question", prompt="你想问什么")
async def handleuser(
        question: Message = Arg()
):
    question = str(question)
    print("输入为：{0}".format(question))
    try:
        answer = await chat2opt(question)
        # answer = "answer" + question
        # msg = f"model({model})回答：\n{answer}"
        msg = answer
    except Exception as e:
        msg = f"发生错误： {str(e)}"
    finally:
        print(msg)
        await chatgpt.finish(msg.strip().replace("\n\n", "\n"))







# while True:
#     prompt = input("提问: ")
#     try:
#         response = chat(prompt)
#     except Exception as e:
#         response = str(e)
#
#     print("ChatGpt: ", response)

