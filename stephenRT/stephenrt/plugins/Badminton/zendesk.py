#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/2/21 16:08
# @Author   : StephenZ
# @Site     : 
# @File     : zendesk.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>


from urllib.parse import urlencode
import requests, json, re
import datetime, time
from nonebot.adapters.onebot.v11 import Bot
from nonebot import get_bot, require

import stephenrt.privateCfg as cfg

scheduler = require("nonebot_plugin_apscheduler").scheduler
config = cfg.config_content

credentials = config["zen_cred1"], config["zen_cred2"]
session = requests.Session()
session.auth = credentials
domain = config["zen_url"]
user_id = config["user_id"]
group_id = config["group_id"]


def show_ticket(ticketId):
    """
    获取单个
    :param ticketId:
    :return:
    """
    interface = "/api/v2/tickets/{0}".format(ticketId)
    url = domain + interface
    response = session.get(url)
    if response.status_code != 200:
        result = 'Status:' + str(response.status_code) + 'Problem with the request. Exiting.'
    result = response.json()
    return result


def search_tickets(search_string):
    """
    搜索单
    :param search_string: 字符串
    :return:
    """
    params = {
        'query': '{0}'.format(search_string),
        'sort_by': 'created_at',
        'sort_order': 'asc'
    }
    # print(params)
    interface = "/api/v2/search.json?"
    url = domain + interface + urlencode(params)
    # print(url)
    response = session.get(url)
    if response.status_code != 200:
        result = 'Status:' + str(response.status_code) + 'Problem with the request. Exiting.'
    else:
        result = response.json()
        count = result["count"]
        # print("查询共{0}条".format(count))
        # print(json.dumps(result))
    return result


def projectCount(search_string):
    """
    获取单子
    :param search_string: 日期
    :return:
    """
    search_result = search_tickets("created:" + search_string)
    results = search_result["results"]
    print("_____", len(results))
    project = {}
    count = 0
    for ticket in results:
        if ticket["result_type"] == "ticket":  # 还有部分是user的
            count += 1
            subject = ticket["subject"]
            if re.match("\[.*?\]", subject):
                subject = re.search("\[.*?\]", subject).group()[1:-1]
            elif subject == "":
                subject = "无"
            if subject in project.keys():
                project[subject] += 1
            else:
                project[subject] = 1
    project = sorted(project.items(), key=lambda x: x[1], reverse=True)
    # print(project)
    # print("总数：", count)
    return [count, project]


@scheduler.scheduled_job("cron", hour=11, minute=28, second=0)
async def send_message():
    bot = get_bot()
    today = datetime.datetime.now().date().strftime('%Y-%m-%d')
    yesterday = (datetime.datetime.now() + datetime.timedelta(days=-1)).date().strftime('%Y-%m-%d')
    print(today, yesterday)
    # day = str(datetime.date.today())
    # 处理msg打印
    yTickets = projectCount(str(yesterday))
    tTickets = projectCount(str(today))
    change = "增长" if tTickets[0] > yTickets[0] else "减少"
    change_no = '{:.2%}'.format((tTickets[0] - yTickets[0]) / yTickets[0])
    msg = "Zendesk 今日工单：{0}，昨日{1}， 同比{2} {3} \n".format(tTickets[0], yTickets[0], change, change_no)
    for project_data in tTickets[1]:
        msg = msg + "{0}: {1}".format(project_data[0], project_data[1]) + "\n"

    # print(msg)

    try:
        await bot.send_group_msg(group_id=group_id, message=msg)
    except Exception as e:
        await bot.send_private_msg(user_id=user_id, message=str(e))
        await bot.send_private_msg(user_id=user_id, message=str(msg))


