#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/2/16 8:28
# @Author   : StephenZ
# @Site     : 
# @File     : test.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>
import requests, json, random, time
from lxml import etree
import re


base_url = "tapd.cn"

search_url = "https://www.tapd.cn/api/search_filter/search_filter/search"

