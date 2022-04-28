#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/4/22 17:39
# @Author   : StephenZ
# @Site     : 
# @File     : test1.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import requests, json
import websockets
import asyncio

socket_url = "ws://10.10.10.21:3002/chatRoom"
# base_url = "http://10.10.10.21:3000/login"
# test_user = {"user": "zhangjian", "pass": "zhangjian2705"}

msg_list = []

async def chat_message():
    async with websockets.connect(socket_url) as socket:
        while True:
            recieve = await socket.recv()
            # await asyncio.sleep(1)
            msg_list.append(recieve)
            print(recieve)
            print(type(recieve))
# def get_chats():
#     print("聊天获取")
#     payload = {}
#     try:
#         with requests.session() as session:
#             session.post(url=base_url, data=test_user)
#             print("session:", session)
#     except Exception as e:
#         print(e)
#         return str(e)

async def deal_message():
    await chat_message()
    print()
    return msg_list


loop = asyncio.get_event_loop()
loop.run_until_complete(deal_message())
loop.close()