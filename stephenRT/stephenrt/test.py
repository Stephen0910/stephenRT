#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/2/16 8:28
# @Author   : StephenZ
# @Site     : 
# @File     : test.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>
import requests, json
import asyncio

v_url = "https://api.linhun.vip/api/Littlesistervideo?type=json"


async def get_video():
    with requests.get(v_url) as session:
        response = session.text
        data = json.loads(response)["video"]
        print(data)
    return data


loop = asyncio.get_event_loop()
loop.run_until_complete(get_video())
loop.close()
