#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/10/20 10:31
# @Author   : StephenZ
# @Site     : 
# @File     : st.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import json, requests, datetime, time
import asyncpg
import asyncio
from google_play_scraper import app
import logzero, logging
from logzero import logger
import psycopg2
from psycopg2.extras import RealDictCursor

logzero.loglevel(logging.DEBUG)
proxy = "127.0.0.1:7890"

proxies = {
    'http': 'http://' + proxy,
    'https': 'http://' + proxy
}

payload = {}
headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    # 'Cookie': 'locale=zh-CN; _ga=GA1.2.203696473.1660202575; _biz_uid=a505c8e68b944d99d391dbb0274dac83; _mkto_trk=id:351-RWH-315&token:_mch-sensortower-china.com-1660202575885-51368; _biz_flagsA=%7B%22Version%22%3A1%2C%22ViewThrough%22%3A%221%22%2C%22XDomain%22%3A%221%22%2C%22Mkto%22%3A%221%22%7D; sliguid=8160e4d8-378a-487f-ab95-862c760bb8bb; slirequested=true; _biz_nA=18; _biz_pendingA=%5B%5D; session=31691928a0a1ae5dc44bcc1047fa5a7a; _gid=GA1.2.20007799.1666171104; amplitude_id_6edb64137a31fa337b6f553dbccf2d8bsensortower-china.com=eyJkZXZpY2VJZCI6ImZjNTcwM2E0LWIxNTQtNDY4YS1iYWRiLTFhZTRhYWQ2ZjQ0YVIiLCJ1c2VySWQiOiJqaWFuemhhbmcwOTEwQGdtYWlsLmNvbSIsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTY2NjE3MTEwMTk0NiwibGFzdEV2ZW50VGltZSI6MTY2NjE3MTExNzI2NCwiZXZlbnRJZCI6NDEsImlkZW50aWZ5SWQiOjIsInNlcXVlbmNlTnVtYmVyIjo0M30=; locale=zh-CN',
    'If-None-Match': 'W/"e9876d0b23096f8595dd7213acaa1b65"',
    'Referer': 'https://app.sensortower-china.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'X-CSRF-Token': 'bTwJgyPw3cB/zYUvJYfxWHuBt9ewnYkSaqJpsn+DpYu4+i5WvsVpQMSPpUT/a+9j01wSfPMCnG3YbcT4Wx7TfA==',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}

if __name__ == '__main__':
    from local_config import *
else:
    from .local_config import *


def save_json(game_id, json_data):
    """
    执行插入sql
    :param sql:
    :return:
    """
    column_sql = "game_id,"
    value_sql = f"{game_id}, "
    update = int(time.time())
    with psycopg2.connect(user=pgsql["user"], password=pgsql["password"], database=pgsql["database"],
                          host=pgsql["host"]) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            select_sql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = 'projects_st'"
            cursor.execute(select_sql)
            columns = cursor.fetchall()
            for i in columns:
                column = i["column_name"]
                if column in json_data.keys():
                    # logger.debug(json_data[column])
                    column_sql = column_sql + f"{column},"
                    column_value = str(json_data[column]).replace("'", "\"")
                    value_sql = value_sql + f"'{column_value}',"
            column_sql += "update"
            value_sql += f"{update}"
            insert_sql = f"INSERT INTO projects_st ({column_sql}) VALUES ({value_sql});"

            try:
                cursor.execute(insert_sql)
                conn.commit()
            except Exception as e:
                logger.error("sql执行失败：\n{0}\n{1}".format(str(e), insert_sql))


def select_data(sql):
    """
    执行select sql
    :param sql:
    :return:
    """
    # conn = psycopg2.connect(user=pgsql["user"], password=pgsql["password"], database=pgsql["database"],
    #                              host=pgsql["host"])
    with psycopg2.connect(user=pgsql["user"], password=pgsql["password"], database=pgsql["database"],
                          host=pgsql["host"]) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(sql)
            data = cursor.fetchall()
    return data


def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    return yesterday


def app_info(platform, app_id):
    """
    获取app信息
    :param platform:
    :param app_id:
    :return:
    """
    url = f"https://app.sensortower.com/api/{platform}/apps/{app_id}"
    with requests.get(url, data=payload, headers=headers, proxies=proxies) as response:
        if response.status_code == 200:
            data = json.loads(response.text)
        else:
            data = f"{app_id} {platform} app_info 获取失败"
        return data


def rank_info(platform, app_id, country="us"):
    """
    获取排行榜信息
    :param platform:
    :param app_id:
    :param country:
    :return:
    """
    category_url = f"https://app.sensortower.com/api/{platform}/category/app_category_ranking_summary?app_ids={app_id}"
    with requests.get(category_url, data=payload, headers=headers, proxies=proxies) as response:
        if response.status_code == 200:
            data = json.loads(response.text)
            categories = data["categories"]
            chart_types = data["chart_types"]
            rank_cate_elem = "".join([f"categories%5B%5D={x}&" for x in categories])
            chart_type_elem = "".join([f"chart_type_ids%5B%5D={x}&" for x in chart_types])
            rank_url = f"https://app.sensortower.com/api/{platform}/category/category_history?app_ids%5B%5D={app_id}&{rank_cate_elem}&{chart_type_elem}&countries%5B%5D={country}&end_date={str(datetime.date.today())}&start_date={getYesterday()}"
            with requests.get(rank_url, data=payload, headers=headers, proxies=proxies) as response:
                if response.status_code == 200:
                    data = json.loads(response.text)
                    logger.debug(json.dumps(data))
                    return data
                else:
                    return f"{app_id}获取rank失败"
        else:
            return f"{app_id}获取目录失败"


def local_apps():
    """
    获取数据库的game_info
    :return:
    """
    app_sql = "SELECT * FROM game_info WHERE is_pulish is True order by game_id"
    result = select_data(app_sql)
    # game_ids = [x["game_id"] for x in result]
    # logger.debug(game_ids)
    logger.debug(result)
    return result


if __name__ == '__main__':
    android = "slots.machine.winning.android"
    ios = "1330550298"
    badminton = "1546338773"

    # info = app_info("ios", ios)
    # save_json(101, info)
    local_apps()
    # rank_info("android", "endless.nightmare.shrine.horror.scary.free.android", "IN")
    # rank_info("ios", badminton, "cn")

    # android_info("ios", ios)
    # print(datetime.date.today())
    # print(getYesterday())
