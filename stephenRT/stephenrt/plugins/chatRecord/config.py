#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/1/30 10:48
# @Author   : StephenZ
# @Site     : 
# @File     : config.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2020>
import json
import os

def get_config():
    up_dir = os.path.abspath(os.path.join(os.getcwd(), "../../"))
    config_path = os.path.join(up_dir, "config.json")
    with open(config_path, "r") as f:
        config_content = json.load(f)
        # print(config_content, type(config_content))
        return config_content