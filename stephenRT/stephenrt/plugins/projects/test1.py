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

import requests, json
import websockets
import asyncio
import re
import os, subprocess



from requests_html import HTMLSession
session = HTMLSession()
proxy="http://127.0.0.1:7890"


from bs4 import BeautifulSoup
import requests, lxml, re, json
from datetime import datetime

# user-agent headers to act as a "real" user visit

with requests.session("https://accounts.google.com/", password) as session:
    print(session.text)
