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
from nonebot.adapters.onebot.v11 import MessageEvent
from nonebot.params import Depends
import stephenrt.privateCfg as cfg

config = cfg.config_content
players = [281016636, 659738900, 158709003, 726408753, 378282033, 675246207, 3274888291]


openai.api_key = config["openai"]

print("chatgpt 加载成功")

chatgpt = on_command("op", rule=to_me(), aliases={"cg", "ai", "请问", "你知道", "知道", "知不知道", "问"}, priority=1 )

# model = "text-davinci-003"
model = "gpt-3.5-turbo-0301"
# model = "text-davinci-002"

proxies = {
    'http': '127.0.0.1:7890',
    'https': 'https://<proxy_host>:<proxy_port>'
}



async def chat2opt(prompt):
    # completions = openai.Completion.create(
    #     #     engine=model,
    #     #     prompt=prompt,
    #     #     max_tokens=1024,
    #     #     n=1,
    #     #     stop=None,
    #     #     temperature=0,
    #     # )
    #     #
    #     # message = completions.choices[0].text
    #     # return message
    response = await openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0301",  # gpt-3.5-turbo-0301
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        proxies = proxies
    )
    # print(response)
    return response.choices[0].message.content


async def depend(event: MessageEvent):  # 2.编写依赖函数
    return {"uid": event.get_user_id(), "nickname": event.sender.nickname}


@chatgpt.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg("question", args)  # 如果用户发送了参数则直接赋值  


@chatgpt.got("question", prompt="你有什么问题？（输入取消/放弃 放弃会话）")
async def handleuser(
        question: Message = Arg(), x: dict = Depends(depend)
):
    question = str(question)
    print("输入为：{0}".format(question))
    if question in ["取消", "放弃"]:
        await chatgpt.finish("已结束会话")
    # if int(x["uid"]) in players:
    if "1" == "1":
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
    else:
        print(str(x["uid"]) + "无权限")


if __name__ == '__main__':
    pass
