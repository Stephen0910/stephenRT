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

b = {
    "code": 0,
    "count": 34,
    "records": [
        {
            "app_type": 2,
            "channel_order_no": "4200001235202106140987504864",
            "count": 500,
            "create_time": "2021-6-14 19:43:31",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200001006202105112625506829",
            "count": 500,
            "create_time": "2021-5-11 20:54:10",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000884202104085470200768",
            "count": 500,
            "create_time": "2021-4-8 16:26:2",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000933202102213197718929",
            "count": 500,
            "create_time": "2021-2-21 14:55:23",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000791202101058941795218",
            "count": 500,
            "create_time": "2021-1-5 21:14:13",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000752202012072124140162",
            "count": 500,
            "create_time": "2020-12-7 0:44:7",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000728202010173403518727",
            "count": 500,
            "create_time": "2020-10-17 11:52:22",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000688202008292580699319",
            "count": 500,
            "create_time": "2020-8-29 11:10:34",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000529202005173578602025",
            "count": 500,
            "create_time": "2020-5-17 14:46:0",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000488202004069842176032",
            "count": 500,
            "create_time": "2020-4-6 20:43:14",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000492202003100462334435",
            "count": 500,
            "create_time": "2020-3-10 16:40:15",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000473202002067693521405",
            "count": 500,
            "create_time": "2020-2-6 21:37:58",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000439201910147018475532",
            "count": 500,
            "create_time": "2019-10-14 20:29:9",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000392201909288962548503",
            "count": 500,
            "create_time": "2019-9-28 21:18:19",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000378201908259271093185",
            "count": 500,
            "create_time": "2019-8-25 19:56:59",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000393201907241128409618",
            "count": 500,
            "create_time": "2019-7-24 22:23:1",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000334201907123839775732",
            "count": 500,
            "create_time": "2019-7-12 19:31:26",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000313201907017856305164",
            "count": 500,
            "create_time": "2019-7-1 21:32:42",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000315201906096405873724",
            "count": 500,
            "create_time": "2019-6-9 1:8:59",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000326201906014006800090",
            "count": 500,
            "create_time": "2019-6-1 23:27:46",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000313201905253109880355",
            "count": 500,
            "create_time": "2019-5-25 19:39:10",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000312201904273075358318",
            "count": 500,
            "create_time": "2019-4-27 16:33:56",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000282201901254670513315",
            "count": 500,
            "create_time": "2019-1-25 17:54:46",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000231201812305115794458",
            "count": 500,
            "create_time": "2018-12-30 13:0:51",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000224201812030406332579",
            "count": 500,
            "create_time": "2018-12-3 21:12:39",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000179201809235825157159",
            "count": 500,
            "create_time": "2018-9-23 19:8:42",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000163201808302493695992",
            "count": 1000,
            "create_time": "2018-8-30 20:28:39",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000161201808213619727761",
            "count": 500,
            "create_time": "2018-8-21 9:35:39",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000130201807247779563523",
            "count": 500,
            "create_time": "2018-7-24 19:10:11",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000065201802258319788488",
            "count": 100,
            "create_time": "2018-2-25 19:39:0",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000072201802036120252536",
            "count": 100,
            "create_time": "2018-2-3 14:17:50",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200000062201802015108999002",
            "count": 100,
            "create_time": "2018-2-1 23:53:31",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 1,
            "channel_order_no": "2018011321001004790285362979",
            "count": 500,
            "create_time": "2018-1-13 19:25:49",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "支付宝充值"
        },
        {
            "app_type": 1,
            "channel_order_no": "2018011321001004790285245531",
            "count": 190,
            "create_time": "2018-1-13 19:22:21",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "支付宝充值"
        }
    ]
}

c = {
    "code": 0,
    "count": 12,
    "records":
    [
        {
            "app_type": 2,
            "channel_order_no": "4200001373202204128677544245",
            "count": 100,
            "create_time": "2022-4-12 21:51:50",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200001392202204061332147966",
            "count": 100,
            "create_time": "2022-4-6 23:9:29",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200001363202203286884801760",
            "count": 100,
            "create_time": "2022-3-28 21:45:11",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200001367202203234868837519",
            "count": 100,
            "create_time": "2022-3-23 20:37:2",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200001355202203194750703302",
            "count": 100,
            "create_time": "2022-3-19 16:23:30",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200001379202203142090778796",
            "count": 100,
            "create_time": "2022-3-14 19:2:11",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200001404202203050655943735",
            "count": 100,
            "create_time": "2022-3-5 16:48:24",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200001374202202278681064161",
            "count": 100,
            "create_time": "2022-2-27 21:14:58",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200001360202202210216990565",
            "count": 100,
            "create_time": "2022-2-21 23:11:37",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200001403202202177328920692",
            "count": 100,
            "create_time": "2022-2-17 20:16:25",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200001412202202116439324134",
            "count": 100,
            "create_time": "2022-2-11 22:47:36",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        },
        {
            "app_type": 2,
            "channel_order_no": "4200001371202201204272762274",
            "count": 100,
            "create_time": "2022-1-20 18:48:13",
            "rollback_flag": 0,
            "rollback_reason": "",
            "channel": "微信充值"
        }
    ]
}

count = 0
for i in c["records"]:
    count += i["count"]
print(count)

b = """
https://shop.09game.com/shop?{"type":"q_my_charge","json":"{\"Days\":30,\"Token\":\"54833-e4bda0e5a5bde5b0b9e5a4a9e4bb87-65536-1649903651-206_2-51e0ce60d8b6bb088bfac56ca76f9739\",\"Start\":0,\"Count\":12}"}
""".encode("utf-8")
print(b)
