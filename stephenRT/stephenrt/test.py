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

import re

a = "[Badminton Blitz][GOOGLE][59ed75222d1946deac86165f5276e614] - SUPPORT"
print(re.search("\[.*?\]", a).group()[1:-1])
