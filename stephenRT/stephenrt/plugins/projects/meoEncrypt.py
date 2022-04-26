#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/4/22 15:35
# @Author   : StephenZ
# @Site     : 
# @File     : meoEncrypt.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import requests, random, time
from lxml import etree
import re
import json, base64
import zlib, gzip
import gzip
# py2导入方法
# import StringIO

orin_data = "H4sIAP6QYmIA{03LTQ7CIBBA4bvMWgiUmtJephmHoSXKT4B0Y7y77HT75b03lBd2n2uEDTC5moODGxSkJx48LCKdIYXWJadwRJQRO53GV2b567GU{eLaQk7j0dLI.9DK7U{VEMdXIN7Hs4E3zrpVz4LJkpiVVwLtA8XimSbWq1t4gs8XZuaZUKEAAAA}"
# print("orin_data：\n", orin_data)

a = "H4sIAAAAAAAAA52W0a6iMBCG34Vrs7p656tsNk0tI3QtbdMWOOTEdz9F0A6IYdjECyH{{7XMdGb6nfnAQ.2z82GXOVMHcExJH7Lzn.{sBl12zpQppM52We1UfCpDsOf9{vfh1{A7Hk{n0.Fw2A.y..5puwLkFy5u686XMpmFM5pBxaVatyNtAtRWGZ4z7kQpG1iHzPRvIKt4F0Mj9dWQYdiTgAUEphrmuCaE5iGGBtSgn1KI8XlJj8hvLJADnLSYkMfnjvGWu5z1S9BCs.hahgrFZbWNOFgSzlupiRtL0qmd5sSmTotxO5Z3tApY8ExTPVam5aGkJRwb8GHOeQDmQecMNLiioxzmN08CliawUSBKoHzqm2P6oQ1XMpahCLKRgbC7BQ9qQfLrWdFMGH1VUgRCO1pyJWifnSKGN4Yjtrx13EyfQI3MwQxZX6dgMY5YTEgfysK4vG81BNKCB.0JnLx2W3BvDrS74V08g4JyarF6eih8aSyxjKfyKabgVTzHraRtZ2ZIKAcX4zQbMjJOz1XckukDsh8bG4EPyyxm4GJqWJAVxOUqSwzd3JWgVhbM81gTldHQjTW8Tl22TfeaK7EhvS91gsQJ6bqcdyxwf3u2l{7{OvGz9RP.0WhiEXlPHVEr{o8L9dX.v4tgL1pA56pfuL9NEEP.bvmAG249G4Gj6W1E1X7DbWvmwNeJwFkli0e{I3baBU8CVpBz9egL6yCkRbeD.uKFkzZIQ7laYDX6rBg.cIRR9hQm67.6sqUsCA3wpUS3cqMUCNrWkRbNTvPljCEc5qcQzXJlWnCE6T3o8LwOQYHlntClkTYBNLRsS95n.iloSwhn.gRq4eKNuEE6Aa2fE46n0ym7{73{AIpF7UnhDQAA"

last_data = {"platform": "android", "package": "machinist.enigma.match3free.android", "app_version": "1.3.5",
             "res_version": "0", "device_id": "f3d8d914-ec8c-40f0-a8ba-7fec2e19d7e2"}


def strReplace(isEncode, ret):
    if isEncode is True:
        ret = ret.replace("+", ".")
        ret = ret.replace("/", "{")
        ret = ret.replace("=", "}")
    else:
        ret = ret.replace(".", "+")
        ret = ret.replace("{", "/")
        ret = ret.replace("}", "=")  # eslint - disable - lineno - useless - escape
    return ret


def uncompress(c_data):
    f = StringIO.StringIO(str(c_data))
    # gziper = gzip.GzipFile(fileobj=f, compresslevel=9)
    # data2 = gziper.read()  # 读取解压缩后数据
    # gziper.close()
    with gzip.GzipFile(fileobj=f, compresslevel=9) as f:
        data = f.read()
    return data


def decode(deStr):
    rStr = strReplace(False, deStr)
    ret = base64.standard_b64decode(rStr.encode("utf-8"))
    ret = gzip.decompress(ret)  # py3写法
    # ret = uncompress(ret)  # py2写法
    ret = json.loads(ret)
    return ret


# #
# s1 = json.dumps(last_data)
# # print(s1, type(s1))
# #
# s2 = gzip.compress(bytes(s1, encoding="utf-8"))
# # print("字典-字符串-zlib压缩：-------------\n", s2)
#
# s3 = base64.standard_b64encode(s2)
# # print(s3)
#
# s4 = strReplace(True, str(s3, encoding="utf-8"))
# print("加密最终：", s4)
# # print("------------------------------------------------")
# t0 = strReplace(False, orin_data)
#
# t1 = base64.standard_b64decode(t0.encode("utf-8"))  # b64编码 传入utf-8格式的字符串
#
# t2 = gzip.decompress(t1)  # decompress是解压，传入Bytes
# print("解密最终:\n", t2)

b = decode(a)

print(json.dumps(b, sort_keys=False, indent=4, separators=(', ', ': ')))
