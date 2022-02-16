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

import jieba

a = "性能测试的重点是怎么把测试用例梳理出来，而不是白盒测试"
for i in jieba.cut(a, cut_all=True):
    print(i)