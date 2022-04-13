#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/2/15 11:46
# @Author   : StephenZ
# @Site     : 
# @File     : test.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import re

a = {
    "code": 0,
    "count": 27,
    "records": [
        {
            "app_type": 2,
            "channel_order_no": "4200001376202204049508337603",
            "count": 100,
            "create_time": "2022-4-4 14:2:0",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000799202101107187885274",
            "count": 500,
            "create_time": "2021-1-10 18:17:32",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000545202004115260482405",
            "count": 1000,
            "create_time": "2020-4-11 13:25:9",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000472202003314527548937",
            "count": 1000,
            "create_time": "2020-3-31 19:19:31",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000493202003216637949944",
            "count": 1000,
            "create_time": "2020-3-21 22:2:50",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000495202003104782977780",
            "count": 1000,
            "create_time": "2020-3-10 18:55:14",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000493202002268709398670",
            "count": 1000,
            "create_time": "2020-2-26 19:25:43",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000496202002080872951385",
            "count": 1000,
            "create_time": "2020-2-8 13:18:53",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000477202001068185498241",
            "count": 1000,
            "create_time": "2020-1-6 20:42:48",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000396201910021911159514",
            "count": 1000,
            "create_time": "2019-10-2 12:27:39",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000390201908225350305661",
            "count": 1000,
            "create_time": "2019-8-22 19:20:51",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000393201907239137107855",
            "count": 1000,
            "create_time": "2019-7-23 21:59:42",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000326201907119172491150",
            "count": 1000,
            "create_time": "2019-7-11 23:40:47",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000324201906175052527653",
            "count": 1000,
            "create_time": "2019-6-17 22:48:11",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000314201906037432693733",
            "count": 1000,
            "create_time": "2019-6-3 22:23:37",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000324201905221000741504",
            "count": 1000,
            "create_time": "2019-5-22 10:18:55",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000311201905119558738722",
            "count": 1000,
            "create_time": "2019-5-11 15:3:1",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000312201904204745372209",
            "count": 1000,
            "create_time": "2019-4-20 11:13:5",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000225201812289913162662",
            "count": 1000,
            "create_time": "2018-12-28 21:24:49",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000212201811243352803645",
            "count": 1000,
            "create_time": "2018-11-24 20:18:22",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000225201810246731204731",
            "count": 1000,
            "create_time": "2018-10-24 21:59:17",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000171201809241554809496",
            "count": 1000,
            "create_time": "2018-9-24 17:29:58",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000163201809151550123957",
            "count": 1000,
            "create_time": "2018-9-15 22:44:11",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000167201809021005387265",
            "count": 1000,
            "create_time": "2018-9-2 18:52:46",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000184201808261974860672",
            "count": 1000,
            "create_time": "2018-8-26 16:12:36",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000137201807169428533009",
            "count": 1000,
            "create_time": "2018-7-16 22:19:54",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000122201807021636246071",
            "count": 1000,
            "create_time": "2018-7-2 19:25:12",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        }
    ]
}

count = 0
for i in a["records"]:
    count += i["count"]
print(count)

b = """
https://shop.09game.com/shop?{"type":"q_my_charge","json":"{\"Days\":30,\"Token\":\"54833-e4bda0e5a5bde5b0b9e5a4a9e4bb87-65536-1649903651-206_2-51e0ce60d8b6bb088bfac56ca76f9739\",\"Start\":0,\"Count\":12}"}
""".encode("utf-8")
print(b)