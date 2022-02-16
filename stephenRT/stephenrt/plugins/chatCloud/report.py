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
from stephenrt.privateCfg import config_content
import psycopg2
import jieba
from wordcloud import WordCloud
import numpy as np
from PIL import Image
import re, os, sys, datetime
import random

# print(config_content)
config = config_content

# 系统不同字体路径不同
platform = sys.platform
print("platform:", platform)
if platform == "win32":
    fontPath = "C:/Windows/Fonts/msyh.ttc"
else:
    fontPath = "/etc/fonts/msyh.ttc"

# mask蒙版底片
imageMask = "wordcloud.png"


def get_user_dict_file():
    # d = os.path.dirname(os.path.realpath(__file__))
    user_path = os.path.join(os.getcwd(), "stephenrt", "plugins", "chatCloud", "myDict.txt")
    return user_path


def get_user_stop_file():
    # d = os.path.dirname(os.path.realpath(__file__))
    block_path = os.path.join(os.getcwd(), "stephenrt", "plugins", "chatCloud", "stopwords.txt")
    stop_words = [line.strip() for line in open(block_path, 'r', encoding='utf-8').readlines()]
    return stop_words


class Report:
    def __init__(self):
        self.conn = psycopg2.connect(user=config["user"], password=config["password"], database=config["database"],
                                     host=config["host"])
        self.cursor = self.conn.cursor()

    def getRecords(self, group_id, timestamp):
        """
        获取某群聊天记录
        :param group_id:
        :param timestamp:
        :return:
        """
        if re.match("\d+\d", str(group_id)):
            print("输入的类型是数字")
            sql = """SELECT message, sender_id, sender_name, group_card FROM "group" WHERE "group_id" = {0} and "timestamp" > '{1}'""".format(
                group_id, timestamp)
        else:
            print("输入的类型是字符")
            sql = """SELECT message, sender_id, sender_name, group_card FROM "group" WHERE "upper"(group_name) like "upper"('%{0}%') and "timestamp" > '{1}'""".format(
                group_id, timestamp)
        print("recordSql:", sql)
        self.cursor.execute(sql)
        msgs = self.cursor.fetchall()
        self.conn.close()
        return msgs

        # def normalTime(self, timestamp):

    #     dateArray = datetime.datetime.utcfromtimestamp(int(timestamp) + 8 * 3600)  # 时区加8)
    #     msg_time = dateArray.strftime("%Y-%m-%d %H:%M:%S")
    #     return msg_time

    def wordReport(self, group_id, timestamp):
        """
        提取词排行
        :param group_id:
        :param timestamp:
        :return:
        """
        words = self.getRecords(group_id, timestamp)
        # print("words:", words)
        words_lenth = len(words)
        print("消息共{0}条".format(words_lenth))
        # 处理关键词累计
        msgs = [word[0] for word in words]
        # 结巴分词将信息分词，并组成列表
        top_dic = {}
        wordText = ""
        # 需要处理部分自定义词，避免切割
        jieba.load_userdict(get_user_dict_file())
        for msg in msgs:
            # 正则非贪婪模式 过滤CQ码
            msg = re.sub('\[CQ:\w+,.+?\]', '', msg, flags=re.S)
            # 过滤URL
            msg = re.sub('(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]', '', msg)
            # 过滤换行符
            msg = msg.replace("\n", "").replace("\r", "")
            # 特殊情况过滤
            msg = msg.replace('&#91;视频&#93;你的QQ暂不支持查看视频短片，请升级到最新版本后查看。', '')
            if "亲爱的友友们" in msg in msg:  #移除客服的开始结束语
                continue
            # if "xml" in msg:
            #     continue
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

        # 去除不统计的词，一般是无意义的
        word_use = []
        print("wordtop:", word_top)
        uselesswords = get_user_stop_file()
        print(uselesswords)
        for word in word_top:
            if word[0] in uselesswords:
                pass
            else:
                word_use.append(word)


        print("word_use:", word_use[:20])
        # 取80个关键词，不够就取完
        try:
            wordDict = dict(word_use[:80])
        except:
            print("关键词不足")
        # topword 前三统计
        top_word = dict(sorted(wordDict.items(), key=lambda x: x[1], reverse=True)[:5])
        top_word_str = "【关键词Top5】\n"
        for key, value in top_word.items():
            top_word_str = top_word_str + "{0}: {1}次\n".format(key, value)

        # 处理玩家发言累计
        upplayer = {}
        for word in words:
            if word[1] not in upplayer:
                upplayer[word[1]] = 1
            else:
                upplayer[word[1]] += 1
        top_player = sorted(upplayer.items(), key=lambda x: x[1], reverse=True)[:3]
        top_player_list = [list(x) for x in top_player]
        print("top_player_list:", top_player_list)
        for player in top_player_list:
            for word in words:
                if player[0] == word[1]:
                    player.append(word[3])
                    player.append(word[2])
                    break
        print(top_player_list)
        top_player_str = "从{2}到目前，统计聊天共{0}条\n{1}【发言Top3】：\n".format(words_lenth, top_word_str, timestamp)
        for player in top_player_list:
            if player[2] == "":
                name = player[3]
            else:
                name = player[2]
            id = player[0]
            count = player[1]
            top_player_str = top_player_str + name + "({0})".format(id) + ":{0}条".format(count) + "\n"
        print("top_player_str:", top_player_str)

        return [wordDict, top_player_str]

    def createPic(self, group_id, timestamp):
        """
        生成词云，报告
        :param group_id: id或查询的信息
        :param timestamp:
        :return:
        """
        cloud_id = random.randint(1,7)
        print("cloud_id:", cloud_id)
        print("random:", cloud_id)
        info = self.wordReport(group_id, timestamp)
        wordDict = info[0]
        top_player = info[1]
        # 蒙版位置
        updir = os.path.abspath(os.path.join(os.getcwd(), "stephenrt", "cloud_base"))
        maskPath = os.path.join(updir, "wordcloud{0}.png".format(cloud_id))
        mask = np.array(Image.open(maskPath))
        wc = WordCloud(font_path=fontPath, mask=mask, background_color='white')
        if len(wordDict) == 0:
            print("没有信息")
            return ["信息太少或群号不正确，请检查", "生成图片失败"]
        wc.generate_from_frequencies(wordDict)
        savePath = os.path.join(updir, ".output", "wordcloud_{0}.png".format(group_id))
        wc.to_file(savePath.format(group_id))
        # 图片位置
        imageInfo = os.path.join(os.getcwd(), savePath)  # 以上图片信息
        return [top_player, imageInfo]


# r = Report()
# r.createPic(645286417, "2022-02-1 9:43:43")
