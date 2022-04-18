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
import requests

total = "https://fuliba2021.net/flhz/page/1"

single = "https://fuliba2021.net/2022053.html/3"
s = requests.get(total)

s.close()
print(s.text)