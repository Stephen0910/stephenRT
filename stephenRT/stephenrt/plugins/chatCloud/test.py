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

msg = """[Badminton Blitz][GOOGLE][1b2f782081d44579a989695103632e50] - SUPPORT"""

project = re.match("\[.*?\]", msg).group()[1:-1]
print(project)
