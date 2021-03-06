#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/4/11 12:25
# @Author   : StephenZ
# @Site     : 
# @File     : __init__.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>
import socket


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


# from .dGame import *
# from .dm_pro.live import *
from .search_body import *
from .nba.season import *
ip = str(get_host_ip())

if ip == "10.10.10.8":
    print("本地内网")
    from .dGame import *
    from .search_body import *
    from .dm_pro.live import *
    from .dm_pro.giftNoti import *
    from .nba.season import *




