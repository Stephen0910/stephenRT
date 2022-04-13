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

# import re
#
# msg = """[Badminton Blitz][GOOGLE][1b2f782081d44579a989695103632e50] - SUPPORT"""
#
# project = re.match("\[.*?\]", msg).group()[1:-1]
# print(project)

def test(id):
    if id <= 0:
        return 0
    t1 = id & 255
    t2 = id >> 8 & 255
    t3 = id >> 16 & 255
    t4 = id >> 24 & 255
    return chr(t4)+chr(t3)+chr(t2)+chr(t1)


a = 1093677364
print(test(a))
