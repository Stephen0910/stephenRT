#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/5/12 11:21
# @Author   : StephenZ
# @Site     : 
# @File     : dm_info.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import requests, json

a = "https://www.doseeing.com/data/api/topuser/5645739?type=gift&dt=7"

# s = requests.get(a)
# print(s.text)
# s.close()

dis_time = [0, 1, 7]


def get_id(user_name):
    with requests.get("https://www.doseeing.com/api/suggest_all?type=room&nickname={0}".format(user_name)) as session:
        data = session.text

    data = json.loads(data)
    rooms = data["suggest"]["room"]
    fans = data["suggest"]["fan"]
    r_uid = dict(zip([x["nickname"] for x in rooms], [x["user_id"] for x in rooms]))
    f_uid = dict(zip([x["nickname"] for x in fans], [x["user_id"] for x in fans]))
    return [r_uid, f_uid]


def get_info(id, count):
    for day in dis_time:
        print("最近{0}天".format(day))
        print("消费：")
        with requests.get("https://www.doseeing.com/data/api/topuser/{0}?type=gift&dt={1}".format(id, day)) as session:
            data = json.loads(session.text)
            for i in data["data"]:
                if i["rank"] < count + 1:
                    print(i["rank"], i["user.nickname"], "￥", i["gift.paid.price"] / 100)
        print("弹幕：")
        with requests.get("https://www.doseeing.com/data/api/topuser/{0}?type=chat&dt={1}".format(id, day)) as session:
            data = json.loads(session.text)
            for i in data["data"]:
                if i["rank"] < count + 1:
                    print(i["rank"], i["user.nickname"], i["chat.pv"], "条")


user_name = "不2不叫"
print(get_id(user_name))

get_info(5264153, 10)
