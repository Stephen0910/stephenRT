#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/4/25 15:21
# @Author   : StephenZ
# @Site     : 
# @File     : bmEncrypt.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>
import gzip, base64
from itertools import cycle
import zlib
from io import BytesIO

encode_data = {
    "platform": "android",
    "package": "machinist.enigma.match3free.android",
    "app_version": "1.3.5",
    "res_version": "0",
    "device_id": "f3d8d914-ec8c-40f0-a8ba-7fec2e19d7e2"
}

decode_data = "OFBtcRhKXkQnBQ1VIBsnY2BPSiMWTBBXDghDXixmYBRkFDsyJCApETtuCBBXWhQbCTotMz4lFg8SXSwJGB0iCD4iMlwOMB1NTFkJCBMdTyJiGE4Wa3NnaSkGLhNEVQdEHBcPcXl6b2AWWVIBaUhzE29JamMoChsdDk0QSw4DD1AcZmIEZhpBc2draFQ6KURZFlIqEQVxeXpvNwsORFByVU0eKgpyIndbWCRIBQMABQ1MRUAjIwYhB3I3cC56VFQx"
print("原数据：", decode_data)


def strReplace(isEncode, ret):
    if isEncode is True:
        # str = str.replace(/\+/gi, '.');
        # str = str.replace(/\//gi, '(');
        # str = str.replace(/=/gi, ')');
        ret = ret.replace(".", "+")
        ret = ret.replace("(", "/")
        ret = ret.replace(")", "=")
    else:
        # str = str.replace(/\./gi, '.+');
        # str = str.replace(/\(/gi, '/');
        # str = str.replace(/\)/gi, '=');
        ret = ret.replace(".+", ".")
        ret = ret.replace("/", "(")
        ret = ret.replace("=", ")")  # eslint - disable - lineno - useless - escape
    return ret


IConfig = {
    "key": bytes("|;(.]dHrU", encoding="utf-8"),
    "keyLength": 50,
    "startPosition": 0,
    "jumpIndex": 1,
    "debug": False
}


def encrypt(orin_bytes):
    config = IConfig["key"]  # 加密字符
    print("config:", config, type(config))
    print("orin_bytes:", orin_bytes)

    j = 0
    ret = BytesIO()
    for one_byte in orin_bytes:
        # print(type(orin_bytes))
        # print("one_byte:", one_byte, type(one_byte))
        # print("config[j]:", config[j], type(config[j]))

        # orin_bytes[j] = one_byte ^ config[j]  # ord返回字符ascii码

        # 异或操作：
        combine = bytes(chr(ord(chr(one_byte)) ^ ord(chr(config[j]))), encoding="utf-8")

        # print("combine:", combine)
        ret.write(combine)
        j += 1
        j %= 9
        # print("j:", j)
    return ret

    # encrypt = [chr(orin_bytes ^ config) for (orin_bytes, b) in zip(orin_bytes, cycle(config))]
    # print(encrypt)


def decode(decode_data):  # 解密
    ret = strReplace(False, decode_data)
    print("1、转换符号后：", ret)
    ret = base64.standard_b64decode(ret)
    print("2、base64压缩后:", ret)
    ret = encrypt(ret)
    print("3、异或加密后：", ret)

    data = ret.getvalue()
    print("获取缓存数据：", data)
    ret.close()
    ret = gzip.decompress(data)

    return ret


print("最终：", decode(decode_data))
