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

import json


pk = "slots.machine.winning.android"

import socks
import socket

socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 7891)
socket.socket = socks.socksocket


from google_play_scraper import app
app = app(pk)
print(json.dumps(app))