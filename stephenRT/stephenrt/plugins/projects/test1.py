#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/4/22 17:39
# @Author   : StephenZ
# @Site     : 
# @File     : test1.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import requests, json
import websockets
import asyncio
import re
import os, subprocess


def run_silently(cmd):
    with os.popen(cmd) as fp:
        bf = fp._stream.buffer.read()
    try:
        return bf.decode().strip()
    except UnicodeDecodeError:
        return bf.decode('gbk').strip()


def run_cmd(cmd):
    with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="gbk") as f:
        data = f.stdout.read()
    return data

print(run_cmd("adb devices"))
