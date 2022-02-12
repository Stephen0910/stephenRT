#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/2/12 17:09
# @Author   : StephenZ
# @Site     : 
# @File     : config.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Author         : yanyongyu
@Date           : 2020-10-04 16:32:00
@LastEditors    : yanyongyu
@LastEditTime   : 2021-09-10 12:42:16
@Description    : None
@GitHub         : https://github.com/yanyongyu
"""
__author__ = "yanyongyu"

from pydantic import BaseSettings


class Config(BaseSettings):
    server_status_only_superusers: bool = True
    server_status_cpu: bool = True
    server_status_per_cpu: bool = False
    server_status_memory: bool = True
    server_status_disk: bool = True

    class Config:
        extra = "ignore"