#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/10/11 10:41
# @Author   : StephenZ
# @Site     : 
# @File     : local_config.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import socket, re


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


ip = get_host_ip()

if re.search("192.*", ip):
    import stephenRT.stephenrt.privateCfg as cfg
else:
    import stephenrt.privateCfg as cfg

pgsql = cfg.config_content
