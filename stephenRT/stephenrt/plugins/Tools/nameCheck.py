#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/6/16 11:48
# @Author   : StephenZ
# @Site     : 
# @File     : nameCheck.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>
import requests
import json

# import requests
#
# url = "http://ga.sczwfw.gov.cn/app/api/convenienceServices/getData"
#
# # payload = "{\"applyId\":\"100101\",\"secretKey\":\"21yuivfp3atyp5vxm5897lua698foy0m\",\"serviceType\":\"cmcx\",\"personName\":\"张一\"}"
# payload = {"applyId":"100101","secretKey":"21yuivfp3atyp5vxm5897lua698foy0m","serviceType":"cmcx","personName":"张一"}
# headers = {
#   'Accept': 'application/json, text/javascript, */*; q=0.01',
#   'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
#   'Connection': 'keep-alive',
#   'Content-Type': 'application/json; charset=UTF-8',
#   'Cookie': 'police=7db761f5de34a6c3355d8b309c65e2d8; scgazwfw=node01g1mr4ijfo2h81ufsl9477ln2d186828.node0; areaCode=510000000000; areaName=; areaId=; level=',
#   'Origin': 'http://ga.sczwfw.gov.cn',
#   'Referer': 'http://ga.sczwfw.gov.cn/app/pubSecurity/cmcx',
#   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
#   'X-Requested-With': 'XMLHttpRequest'
# }
# print(payload)
#
# response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
#
# print(response.text)
# 四川 名字有几个

import requests

url = "http://ga.sczwfw.gov.cn/app/api/convenienceServices/getData"

payload = {"applyId": "100101", "secretKey": "21yuivfp3atyp5vxm5897lua698foy0m", "serviceType": "cmcx",
           "personName": "刘波"}
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=UTF-8',
    'Cookie': 'police=7db761f5de34a6c3355d8b309c65e2d8; scgazwfw=node01g1mr4ijfo2h81ufsl9477ln2d186828.node0; areaCode=510000000000; areaName=; areaId=; level=',
    'Origin': 'http://ga.sczwfw.gov.cn',
    'Referer': 'http://ga.sczwfw.gov.cn/app/pubSecurity/cmcx',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

print(json.loads(response.text)["data"]["data"]["data"]["data"][0]["COUNT"])
response.close()