#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/2/15 11:46
# @Author   : StephenZ
# @Site     : 
# @File     : test.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import re
#
# msg = """[Badminton Blitz][GOOGLE][1b2f782081d44579a989695103632e50] - SUPPORT"""
#
# project = re.match("\[.*?\]", msg).group()[1:-1]
# print(project)

# def test(id):
#     if id <= 0:
#         return 0
#     t1 = id & 255
#     t2 = id >> 8 & 255
#     t3 = id >> 16 & 255
#     t4 = id >> 24 & 255
#     return chr(t4)+chr(t3)+chr(t2)+chr(t1)
#
#
# a = 1215723364
# print(test(a))
#
# titles = ["MVP", "杀", "助", "躺", "灵", "僵"]
#
#
# def get_title(a):
#     user_title = ""
#     title_num = str(bin(a))[2:]
#     print(title_num)
#     for index, i in enumerate(title_num[::-1]):
#         if i == "1":
#             user_title += titles[index]
#     return user_title
#
#
# print(get_title(4))

# a = "击杀:20;死亡:10;助攻:13;金钱:32889;金钱占比:27;伤害:69137;伤害占比:29;额外技能1:A170;额外技能2:A189;装备1:1229008948;装备2:1227899225;装备3:1227896386;装备4:1227902808;装备5:1227899189;装备6:1229008947;装备7:1229078863;英雄:H008;等级:25;"
# a = "击杀:11;死亡:19;助攻:7;金钱:19708;金钱占比:21;伤害:51285;伤害占比:23;额外技能1:A323;额外技能2:A468;装备1:1229008948;装备2:1227900746;装备3:1227897178;装备4:0;装备5:1227900506;装备6:1227896137;装备7:1229078854;英雄:H002;等级:25;"
a = "击杀:3;死亡:14;助攻:12;金钱:14080;金钱占比:15;伤害:22883;伤害占比:10;额外技能1:A063;额外技能2:A279;装备1:1227895880;装备2:0;装备3:1229008962;装备4:1227902281;装备5:1227896388;装备6:1227897178;装备7:1229078833;英雄:U000;等级:25;"
hero = re.search("英雄:.*?;", a).group()[-5:-1]
skill1 = re.search("额外技能1:.*?;", a).group()[-5:-1]
print(hero)
print(skill1)