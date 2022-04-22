#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/4/22 15:35
# @Author   : StephenZ
# @Site     : 
# @File     : encrypt.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import requests, random, time
from lxml import etree
import re
import json, base64
import zlib, gzip

orin_data = "H4sIAP6QYmIA{03LTQ7CIBBA4bvMWgiUmtJephmHoSXKT4B0Y7y77HT75b03lBd2n2uEDTC5moODGxSkJx48LCKdIYXWJadwRJQRO53GV2b567GU{eLaQk7j0dLI.9DK7U{VEMdXIN7Hs4E3zrpVz4LJkpiVVwLtA8XimSbWq1t4gs8XZuaZUKEAAAA}"
print("orin_data：\n", orin_data)

last_data = {"platform": "android", "package": "machinist.enigma.match3free.android", "app_version": "1.3.5",
             "res_version": "0", "device_id": "f3d8d914-ec8c-40f0-a8ba-7fec2e19d7e2"}


def strReplace(isEncode, ret):
    if isEncode is True:
        ret = ret.replace("/\./g", "+")
        ret = ret.replace("/\{/g", "/")
        ret = ret.replace("/\}/g", "=")
    else:
        ret = ret.replace(".", "+")
        ret = ret.replace("{", "/")
        ret = ret.replace("}", "=")  # eslint - disable - lineno - useless - escape
    return ret


def strToBase64(s):
    '''
    将字符串转换为base64字符串
    :param s:
    :return:
    '''
    strEncode = base64.b64encode(s)
    return strEncode


s1 = json.dumps(last_data)
print(s1, type(s1))

s2 = zlib.compress(s1.encode("utf8"))
print("字典-字符串-zlib压缩：-------------\n", s2)

s3 = zlib.decompress(s2)
print(s3)

print("------------------------------------------------")
# t1-转64位编码
t0 = strReplace(False, orin_data).encode()
print("转符号string\n", t0)
t1 = base64.standard_b64decode(t0)  # b64编码 传入utf-8格式的字符串
print("base64压缩byte t1：\n", t1)
print(type(t1))

t2 = zlib.compress(t1)  # decompress是解压，传入Bytes
print("zlib 解压:\n", t2)
