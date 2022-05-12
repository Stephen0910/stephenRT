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

import re
name = "1亓拿走22w鉆和s级球拍"
a = "3564837153|2580237802|166345259|3569544846|2927295662|1327004801|万钻|万钴|万砖|万鉆|萬鉆|萬钻|s级|s拍|亓"

print(re.search(a, name.lower()))

if re.search(a, name.lower()) and len(name) > 8:
    print("get")
else:
    print("????????")