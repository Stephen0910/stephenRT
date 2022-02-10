#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/2/10 10:10
# @Author   : StephenZ
# @Site     : 
# @File     : privateCfg.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import json, os

up_dir = os.path.abspath(os.path.join(os.getcwd(), "../../"))
config_path = os.path.join(up_dir, "config.json")

global config_content

with open(config_path, "r") as f:
    config_content = json.load(f)