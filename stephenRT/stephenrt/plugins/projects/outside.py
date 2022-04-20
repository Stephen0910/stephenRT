#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/4/19 11:24
# @Author   : StephenZ
# @Site     : 
# @File     : outside.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>
import requests

def get_response(url):
    response = requests.get(url)
    response.close()
    return response.content

a = get_response("https://winningslotsgame.com/")
print(a)