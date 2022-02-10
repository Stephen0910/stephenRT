#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/2/10 11:48
# @Author   : StephenZ
# @Site     : 
# @File     : report.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>
from .privateCfg import config_content
import psycopg2
import jieba
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import re, os

print(config_content)
config = config_content
fontPath = "C:/Windows/Fonts/msyh.ttc"
imageMask = "wordcloud.png"


class Report:
    def __init__(self):
        self.conn = psycopg2.connect(user=config["user"], password=config["password"], database=config["database"],
                                     host=config["host"])
        self.cursor = self.conn.cursor()

    def getRecords(self, group_id, timestamp):
        sql = """
        SELECT message, sender_id, sender_name, group_card FROM "group" WHERE "group_id" = {0} and "timestamp" > '{1}'
        """.format(group_id, timestamp)
        self.cursor.execute(sql)
        msgs = self.cursor.fetchall()
        self.conn.close()
        return msgs

    def wordReport(self, group_id, timestamp):
        """
        提取词排行
        :param group_id:
        :param timestamp:
        :return:
        """
        words = self.getRecords(group_id, timestamp)
        print("words:", words)
        print("消息共{0}条".format(len(words)))
        msgs = [word[0] for word in words]
        # 结巴分词将信息分词，并组成列表
        top_dic = {}
        wordText = ""
        for msg in msgs:
            # 正则非贪婪模式 过滤CQ码
            msg = re.sub('\[CQ:\w+,.+?\]', '', msg)
            # 过滤URL
            msg = re.sub('(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]', '', msg)
            # 过滤换行符
            msg = msg.replace("\n", "").replace("\r", "")
            # 特殊情况过滤
            msg = msg.replace('&#91;视频&#93;你的QQ暂不支持查看视频短片，请升级到最新版本后查看。', '')

            wordText = wordText + msg
            for word in jieba.cut(msg, cut_all=False):
                if word not in top_dic.keys():
                    top_dic[word] = 1
                else:
                    top_dic[word] += 1

        top_list = sorted(top_dic.items(), key=lambda x: x[1], reverse=True)
        word_top = []
        for word in top_list:
            if len(word[0]) >= 2:
                word_top.append(word)
        # 取50个关键词，不够就取完
        try:
            wordDict = dict(word_top[:80])
        except:
            print("关键词不足")
            wordDict = dict(word_top)
        return wordDict

    def createPic(self, group_id, timestamp):
        # wc = WordCloud(font_path=font_path, margin=1, random_state=1, max_words=300, width=1000, height=700,
        #                background_color='white').generate(self.wordReport(group_id, timestamp)[-1])
        # 蒙版位置
        updir = os.path.abspath(os.path.join(os.getcwd(), "stephenrt"))
        maskPath = os.path.join(updir, "wordcloud.png")
        mask = np.array(Image.open(maskPath))
        wc = WordCloud(font_path=fontPath, mask=mask, background_color='white')
        wordDict = self.wordReport(group_id, timestamp)
        print("wordDict：", wordDict)
        wc.generate_from_frequencies(wordDict)
        savePath = os.path.join(updir, "pictures", "wordcloud_{0}.jpg".format(group_id))
        wc.to_file(savePath.format(group_id))


r = Report()
r.createPic(135313433, "2022-02-9 9:43:43")
