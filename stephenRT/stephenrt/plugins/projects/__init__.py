#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/4/19 11:24
# @Author   : StephenZ
# @Site     : 
# @File     : __init__.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>


import socket
import re

def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

ip = str(get_host_ip())



if re.match("192.*", ip):
    # from .dGame import *
    # from .dm_pro.live import *
    # from .search_body import *
    # from .nba.season import *
    # from .kuake import *
    # from .wPublic import *
    from .query_game import *
    pass

if ip == "10.10.10.8":
    # from .query_game import *
    pass


if ip == "172.24.121.72":
    # from .query_game import *
    pass


