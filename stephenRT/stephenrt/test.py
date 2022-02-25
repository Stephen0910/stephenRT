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

import requests, re

#
# url = "http://10.10.10.21:3000/badmintonCn/user_search_submit"
#
# payload = 'keyword=136246&searchWay=1'
#
# user = {"user": "zhangjian", "pass": "zhangjian2705"}
#
# headers = {
#     'Content-Type': 'application/x-www-form-urlencoded'
# }
#
#
#
# def get_session(url="http://10.10.10.21:3000/login"):
#     session = requests.session()
#     session.post(url, data=user, headers=headers)
#     return session
#
#
# s = get_session()
# response = s.post(url=url, data=payload, headers=headers)
# print(response.content)

s="{0:^5}\t{1:{3}^15}\t{2:{3}^1}\t{3:^1}"
print(s.format("key","value","",chr(12288)))
