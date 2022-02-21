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

a = """大家好，我是993。欢迎大家随时撩我~[CQ:xml,data=<?xml version="1.0" encoding="utf-8"?>
<msg templateID="1" brief="大家好，我是993。欢迎大家随时撩我~" serviceID="104"><item layout="2"><picture cover=""/><title>新人入群</title></item><source/></msg>
,resid=104"""

import re

b = re.sub("大家好，我是.*?resid=104", "", a, flags=re.S)
print(b)