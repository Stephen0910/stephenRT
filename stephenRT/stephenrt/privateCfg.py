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

# 正式
up_dir = os.path.abspath(os.path.join(os.getcwd(), "../../"))
# 调试
# up_dir = os.path.abspath(os.path.join(os.getcwd(), "../../../../../"))
print(up_dir)
config_path = os.path.join(up_dir, "config.json")

global config_content

try:
    with open(config_path, "r", encoding="utf-8") as f:
        config_content = json.load(f)
except:
    with open(config_path, "r", encoding="gbk") as f:
        config_content = json.load(f)