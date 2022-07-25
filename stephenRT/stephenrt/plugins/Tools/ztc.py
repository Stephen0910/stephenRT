#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/7/6 14:46
# @Author   : StephenZ
# @Site     : 
# @File     : ztc.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import requests, json


def get_tc_pic(key):
    pics = []
    tc_url = "https://zhaotaici.cn/php/api/subtitle_seek_api.php?action=seek_all&query={0}&pageNum=0&title_filter=&actor_filter=&director_filter=&is_en=0".format(key)
    with requests.get(tc_url) as session:
        response = json.loads(session.text)
    for item in response["items"]:
        if item["subTableInfo"]["is_imgs_ready"] == "1":
            title = item["subTableItem"]["title"]
            subid = item["sentence"]["sub_id"]
            start = item["sentence"]["json_sub_item"]["start"]
            print(title)
            pic_url = "https://zhaotaici.cn/php/api/cos.php?action=get_img&subid={0}&start={1}".format(subid, start)
            pics.append(pic_url)
    return pics


a = get_tc_pic("我还没上车呢")
for i in a:
    print(i)