#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2019/12/8 0008 14:51
# @Author   : StephenZ
# @Site     : 
# @File     : ssCheck.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2019
# @Licence  :     <@2019>
"""
使用本地代理，get google.com 检查代理是否走通，一旦失败发送邮件到指定邮件。
需要在上级配置 smtp-config.txt文件，包括 smtp server，发件人，授权码，收件人
配置格式为json
"""

import requests
import logzero, logging
from logzero import logger
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import json

logzero.loglevel(logging.DEBUG)
logzero.logfile("../../logfile.log")


class Shadow():
    def __init__(self):
        self.proxies = {"http": "127.0.0.1:1080", "https": "127.0.0.1:1080"}
        self.fail = 0

    def check(self):
        """
        检查网络是否联通
        :return:
        """
        while True:
            try:
                m = requests.get('https://www.google.com', proxies=self.proxies)
                logger.debug("request get response: %s" % m)
                # logger.debug(m.status_code)
                self.fail = 0
            except:
                logger.error("connect failed")
                self.fail += 1

            # if self.fail == 10:
            #     # break  后续操作
            #     try:
            #         self.mail()
            #         logger.debug("mail sent success")
            #     except:
            #         logging.error("mail sent failed.")

            if self.fail != 0:
                logger.debug("fail is %s" % self.fail)
            time.sleep(3)

    def mail(self):
        """
        发送邮件
        计算机名不能为中文，否则会报编码错误，wtf
        :return:
        """
        with open("..\..\smtp-config.txt", "r", encoding='gbk') as f:
            config = f.read()
        logger.debug(config)
        config_json = json.loads(config)
        logger.debug(config_json)
        logger.debug(type(config_json))

        smtp_server = config_json["smtp_server"]
        sender = config_json["sender"]
        password = config_json["password"]
        receiver = config_json["receiver"]
        logger.debug(receiver)

        message = MIMEText('Shadowsocks 连接失败超过30s，检查或重启。可以连接则忽略此邮件', 'plain', 'utf-8')
        message['From'] = Header("Shadow 自动邮件", 'utf-8')  # 发送者
        message['To'] = Header("自动邮件", 'utf-8')  # 接收者
        subject = '节点连接失败'
        message['Subject'] = Header(subject, 'utf-8')

        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)
        server.login(sender, password)
        logger.debug(server)
        server.sendmail(sender, receiver.split(","), message.as_string())
        server.quit()


if __name__ == '__main__':
    s = Shadow()
    s.check()
