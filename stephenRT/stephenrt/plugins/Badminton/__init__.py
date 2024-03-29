#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/2/12 18:33
# @Author   : StephenZ
# @Site     : 
# @File     : __init__.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>
import socket


# from .ban import *
# from .zendesk import *



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

# from .autoBan import *

ip = str(get_host_ip())


if ip == "10.10.10.8":
    print("本地内网")
    # from .autoBan import *  暂关闭
    from ._ban import *
    from .sensitive import *
else:
    print("不加载chatRoom")


if ip == "172.24.121.72":
    print("不加载")
