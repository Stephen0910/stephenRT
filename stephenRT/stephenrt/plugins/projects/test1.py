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

import json
import json_tools

a = {
    "Seller": "HongKong Triple Sevens Interactive Co., Ltd.",
    "Size": "380 MB",
    "Category": "Games",
    "Compatibility":
        {
            "iPhone": "Requires iOS 10.0 or later.",
            "iPad": "Requires iPadOS 10.0 or later.",
            "iPod touch": "Requires iOS 10.0 or later.",
            "Mac": "Requires macOS 11.0 or later and a Mac with Apple M1 chip or later."
        },
    "Languages": "English, Simplified Chinese",
    "Age Rating":
        {
            "17+": "Frequent/Intense Simulated Gambling"
        },
    "Copyright": "© Copyrights @ Triple Sevens Co.,Ltd",
    "Price": "Free",
    "In-App Purchases":
        {
            "Medium Package": "$4.99",
            "Mega Package": "$9.99",
            "Tiny Win Wheel": "$0.99",
            "Small Package": "$2.99",
            "Key for Mega Private Vault": "$9.99",
            "Tiny Package": "$0.99",
            "Weekly VIP Card": "$9.99",
            "Major Win Wheel": "$2.99",
            "Mini Package": "$1.99",
            "Mega Coin Deal": "$9.99"
        }
}
b = {
    "Seller": "HongKong Triple Sevens Interactive Co., Ltd.",
    "Size": "380 MB",
    "Category": "Games",
    "Compatibility":
        {
            "iPhone": "Requires iOS 10.0 or later.",
            "iPad": "Requires iPadOS 10.0 or later.",
            "iPod touch": "Requires iOS 10.0 or later.",
            "Mac": "Requires macOS 11.0 or later and a Mac with Apple M1 chip or later."
        },
    "Languages": "English, Simplified Chinese",
    "Age Rating":
        {
            "17+": "Frequent/Intense Simulated Gambling"
        },
    "Copyright": "© Copyrights @ Triple Sevens Co.,Ltd",
    "Price": "Free",
    "In-App Purchases":
        {
            "Medium Package": "$4.91",
            "Mega Package": "$9.99",
            "Tiny Win Wheel": "$0.99",
            "Small Package": "$2.99",
            "Key for Mega Private Vault": "$9.99",
            "Tiny Package": "$0.99",
            "Weekly VIP Card": "$9.99",
            "Major Win Wheel": "$2.99",
            "Mini Package": "$1.99",

        }
}

a = [
    {
        "status": "ERROR",
        "count": 5
    },
    {
        "status": "SUCCESS",
        "count": 125
    }
]

for i in a:
    if i["status"] == "ERROR":
        step = i["count"]
        break

print(step)
