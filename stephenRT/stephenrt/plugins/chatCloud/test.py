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

msg = """大家好，我是李沐子。欢迎大家随时撩我~[CQ:xml,data=<?xml version="1.0" encoding="utf-8"?>
<msg templateID="1" brief="大家好，我是李沐子。欢迎大家随时撩我~" serviceID="104"><item layout="2"><picture cover=""/><title>新人入群</title></item><source/></msg>
,resid=104]"""

part = r"\[CQ:\w+.*?\s.*?\]"

msg1 = re.findall(pattern=part, string=msg)
print(msg1)
print("\n\n")
msg = re.sub(pattern=part, repl="", string=str(msg), flags=re.S)
print(msg)


