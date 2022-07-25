#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/6/24 16:07
# @Author   : StephenZ
# @Site     : 
# @File     : aihelp.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import requests, json
import time
# from nonebot import require
# require("nonebot_plugin_apscheduler")
# from nonebot_plugin_apscheduler import scheduler



# appkey = ""

def get_res(start, end):
    """
    官方接口
    :param start:
    :param end:
    :return:
    """
    headers = {
        "Content-Type":"application/json"
    }
    url = "https://aihelp.net/open/api/statistics/chat?appkey={0}&nonce={1}&starttime={2}&endtime={3}".format(appkey, int(time.time())*1000, start, end)
    print(url)
    with requests.get(url=url, headers=headers) as session:
        response = session.text
    return json.loads(response)


# a = get_res(1655913600000, 1656000000000)
# print(a)

def get_tags():
    url = "https://aihelp.net/api/stat/tag/getstats"

    payload = "{\"gameId\":7409,\"LanguageId\":[],\"Platform\":[],\"Type\":0,\"StartTime\":\"2022-06-23 00:00:00\",\"EndTime\":\"2022-06-23 23:59:59\",\"PageIndex\":1,\"PageSize\":20,\"xTagName\":[],\"yTagName\":[]}"
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
        'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6InpoYW5namlhbkBqb3lpZW50LmNvbSIsIm5hbWVpZCI6InpoYW5namlhbkBqb3lpZW50LmNvbSIsIlVzZXJJZCI6IjY1MDgiLCJHYW1lSWQiOiI3NDA5IiwiR2FtZU5hbWUiOiLlhrPmiJjnvr3mr5vnkIMiLCJBY2NvdW50SWQiOiIyMzM1IiwiSXNBZG1pbiI6IjAiLCJTZXNzaW9uSWQiOiJiOTFhNzEzOS04ZDIxLWIwMDItOWE5ZS0xMDFhZGFmMGE4OWYiLCJuYmYiOjE2NTYwNTA5NTksImV4cCI6MTY1NjQ4Mjk1OSwiaWF0IjoxNjU2MDUwOTU5fQ.2wjk-b-ibQh4Q_IpsJSu_1SNMiGvL49K3XGbRftPEHs',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': 'AIHelp_SessionId=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6InpoYW5namlhbkBqb3lpZW50LmNvbSIsIm5hbWVpZCI6InpoYW5namlhbkBqb3lpZW50LmNvbSIsIlVzZXJJZCI6IjY1MDgiLCJHYW1lSWQiOiI3NDA5IiwiR2FtZU5hbWUiOiLlhrPmiJjnvr3mr5vnkIMiLCJBY2NvdW50SWQiOiIyMzM1IiwiSXNBZG1pbiI6IjAiLCJTZXNzaW9uSWQiOiJiOTFhNzEzOS04ZDIxLWIwMDItOWE5ZS0xMDFhZGFmMGE4OWYiLCJuYmYiOjE2NTYwNTA5NTksImV4cCI6MTY1NjQ4Mjk1OSwiaWF0IjoxNjU2MDUwOTU5fQ.2wjk-b-ibQh4Q_IpsJSu_1SNMiGvL49K3XGbRftPEHs; __stripe_mid=5cc930fa-0e9b-47f2-89af-a1559557c0095beaf4; .AspNetCore.Session=CfDJ8DlEtPWDgFNLvdNTNeCk%2F%2BAKV9o9Nmx42AoSTsbCP%2Bms2RJKIhYoP9bRJc6vFS9VWeHPpxH7qpRTGZih%2BMhCbiV9mWJjOs8TNhInaHN5eM%2BJEMcTjXMuceNe9Ap6cuT4btO2dvn0NXf91qwkA0EWrIS7XVwMiIoCknEV6yF5yPhi; .AspNetCore.Session=CfDJ8DlEtPWDgFNLvdNTNeCk%2F%2BDyT51f2WVZ7y78wUo4jzHMHGq1WZtSkXxiewLlGOp%2BgTwvzJjCiF36q%2B8LxILuZiOtZPSMpEV9Aw1h03rPKzkMqucl5sJ3A0aSwLCWD9cWgpsiQiUoEbnBK0gNwcFsGHEB0k%2BO5c3YyjExmiEMmB0Q',
        'Origin': 'https://aihelp.net',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'rc': '0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


get_tags()


# @scheduler.scheduled_job("cron", hour="*/2", id="xxx", args=[1], kwargs={"arg2": 2})
# async def run_every_2_hour(arg1, arg2):
#     pass
#
# scheduler.add_job(run_every_day_from_program_start, "interval", days=1, id="xxx")