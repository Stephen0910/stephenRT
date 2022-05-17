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
# !/usr/bin/env python3
# coding: utf-8

msg_dict = {
    "type": "dgb",
    "rid": "71415",
    "gfid": "824",
    "gs": "0",
    "uid": "184514619",
    "nn": "鬼王丨矜羯罗",
    "ic": "avatar_v3@S201810@S9816f948d8afb874dd89646c9459bf9a",
    "eid": "0",
    "eic": "0",
    "level": "32",
    "dw": "0",
    "gfcnt": "10",
    "hits": "10",
    "bcnt": "1",
    "bst": "7",
    "ct": "14",
    "el": "",
    "cm": "0",
    "bnn": "冷寨主",
    "bl": "17",
    "brid": "107053",
    "hc": "a166c3136d2ab1d77b44a04db94a622f",
    "sahf": "0",
    "fc": "0",
    "cbid": "647203",
    "gpf": "1",
    "pid": "268",
    "bnid": "1",
    "bnl": "1",
    "receive_uid": "2488316",
    "receive_nn": "寅子",
    "from": "2",
    "pfm": "21482",
    "pma": "180907425",
    "mss": "180907447",
    "bcst": "1"
}

sql = """
                        INSERT INTO "public"."dm" ("timestamp", "user_id", "nn", "gfid", "gfn", "icon", "room_id", "room_user", "num", "single_price", "price")
                            VALUES
                        ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', {6}, '{7}', '{8}', {9}, {10});""" % \
      (1, msg_dict["uid"], msg_dict["nn"], msg_dict["gfid"], 2, 2, 2,
       msg_dict["rid"], msg_dict["gfcnt"], 2, 3)
print("sql:", sql)
