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

a = """get_type: <class 'method'> <bound method Event.get_type of GroupMessageEvent(time=1645094566, self_id=2969505561, post_type='message', sub_type='normal', user_id=281016636, message_type='group', message_id=-743898255, message=[MessageSegment(type='text', data={'text': 'sf'}), MessageSegment(type='image', data={'file': 'ec8dbb7d08e81eddfb6c949faeeb9448.image', 'url': 'https://gchat.qpic.cn/gchatpic_new/281016636/755489024-3060637992-EC8DBB7D08E81EDDFB6C949FAEEB9448/0?term=3', 'subType': '1'}), MessageSegment(type='face', data={'id': '294'}), MessageSegment(type='text', data={'text': 'ff'})], raw_message='sf[CQ:image,file=ec8dbb7d08e81eddfb6c949faeeb9448.image,subType=1][CQ:face,id=294]ff', font=0, sender=Sender(user_id=281016636, nickname='张', sex='unknown', age=0, card='非机器人', area='', level='', role='owner', title=''), to_me=False, reply=None, group_id=755489024, anonymous=None, message_seq=2172)>
"""
import re

b = [x[2:] for x in re.findall("=\'text|=\'image|=\'json|=\'face", a)]
print(b)