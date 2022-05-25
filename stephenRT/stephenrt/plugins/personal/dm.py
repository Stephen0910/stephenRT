#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2022/5/11 9:31
# @Author   : StephenZ
# @Site     :
# @File     : dm.py
# @Purpose  :
# @Software : PyCharm
# @Copyright:   (c) StephenZ 2022
# @Licence  :     <@2022>

import websocket
import threading
import requests
import json
from logzero import logger
import logzero, logging
import psycopg2
import socket
import os

import time, datetime
import random

logzero.loglevel(logging.DEBUG)
logger.info("dm start")

user = "other"
if user == "a8":
    id = "5645739"
elif user == "dog":
    id = "5264153"
elif user == "599":
    id = "5106536"
elif user == "pao":
    id = "6566346"
elif user == "kai":
    id = "6974685"
elif user == "pis":
    id = "90016"
else:
    id = "71415"

rooms = {"5645739": "a824683653", "5264153": "肖璐s"}

defalt_lenth = 39
robot = False  # True为打开
free = False  # True为打开免费礼物
save_sql = False
debug = False

# freeGifts = ["粉丝荧光棒"]


# 一些接口可以获取是否在线等情况
# room_info = "https://www.douyu.com/roomapi/biz/getSwitch?rid={0}".format(id)
# loop_info = "https://www.douyu.com/wgapi/live/liveweb/getRoomLoopInfo?rid={0}".format(id)
# is_live = "https://www.douyu.com/wgapi/live/liveweb/roomInfo/expand?rid={0}".format(id)
# play_info = "https://www.douyu.com/lapi/live/getH5Play/{0}".format(id)
# betward = "https://www.douyu.com/betard/{0}".format(id)

def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def get_cfg():
    up_dir = os.path.abspath(os.path.join(os.getcwd(), "../../../../../"))
    config_path = os.path.join(up_dir, "config.json")
    print(config_path)

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config_content = json.load(f)
    except:
        with open(config_path, "r", encoding="gbk") as f:
            config_content = json.load(f)
    return config_content


ip = get_host_ip()
if ip == "10.10.10.8":
    cfg = get_cfg()
    pgsql = cfg
    save_sql = True
    free = False
    debug = True


def isChinese(ch):
    if ch >= '\u4e00' and ch <= '\u9fa5':
        return True
    else:
        return False


def get_time():
    dateArray = datetime.datetime.utcfromtimestamp(time.time())  # 时区加8 不加了
    msg_time = dateArray.strftime("%Y-%m-%d %H:%M:%S")
    return msg_time


def lenStr(string):
    count = 0
    for line in string:
        if isChinese(line):
            count = count + 2
        else:
            count = count + 1
    return count


def save_info(sql):
    """
    执行插入sql
    :param sql:
    :return:
    """
    print(pgsql)
    with psycopg2.connect(user=pgsql["user"], password=pgsql["password"], database=pgsql["database"],
                          host=pgsql["host"]) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)


class DyDanmu:
    def __init__(self, roomid, url, login_name, login_id):
        self.gift_dict = self.get_gift_dict()
        self.price_dict, self.pic_dic = self.get_price_dict()[0], self.get_price_dict()[1]
        # for key, value in self.price_dict.items():
        #     if value > 500000:
        #         print(self.gift_dict[str(key)], key, value)
        # print("礼物：", self.gift_dict)
        # print("价格：", self.price_dict)
        self.login_name = login_name
        self.login_id = login_id
        self.gift_dict_keys = self.gift_dict.keys()
        self.room_id = roomid
        self.client = websocket.WebSocketApp(url, on_open=self.on_open, on_error=self.on_error,
                                             on_message=self.on_message, on_close=self.on_close)
        self.heartbeat_thread = threading.Thread(target=self.heartbeat)
        self.ws = None
        self.name = "【{0}】 ".format(rooms[roomid])


    def start(self):
        self.client.run_forever()

    def stop(self):
        self.logout()
        self.client.close()

    def on_open(self):
        self.login()
        self.join_group()
        self.heartbeat_thread.setDaemon(True)
        self.heartbeat_thread.start()

    def on_error(self, error):
        print(error)

    def on_close(self):
        print('close')

    def send_msg(self, msg):
        msg_bytes = self.msg_encode(msg)
        self.client.send(msg_bytes)

    def on_message(self, msg):
        message = self.msg_decode(msg)
        # print(message)
        for msg_str in message:
            msg_dict = self.msg_format(msg_str)
            # print("-----------", msg_dict)
            if debug is True:
                logger.debug(msg_dict)
            if msg_dict['type'] == 'chatmsg':
                msg = msg_dict["txt"]
                # logger.debug(msg_dict)
                if msg_dict["bnn"] != "":
                    user_info = self.name + "{0}[Lv{1}][{2} {3}] {4}".format("", msg_dict["level"],
                                                                             msg_dict["bnn"], msg_dict["bl"],
                                                                             msg_dict["nn"])
                else:
                    user_info = self.name + "{0}[lv{1}] {2}".format("", msg_dict["level"], msg_dict["nn"])

                if "dms" not in msg_dict.keys():  # dms 机器人？
                    user_info = self.name + "[机器人]" + user_info
                    msg = "\033[1;47m{0}\033[0m!".format(msg)
                    # user_info = ""

                if "rg" in msg_dict.keys() and int(msg_dict["rg"]) == 4:
                    fang = "[房]"  # 是否显示房管
                    # user_info = fang + user_info
                user_info += "："
                # if len(user_info) > 38:
                #     # print("过长..", len(user_info))
                #     user_info = user_info[:34] + ".."
                user_info = user_info + " " * abs(defalt_lenth - lenStr(user_info))

                if robot is False:
                    if "机器人" not in user_info:
                        logger.debug(user_info + msg)
                else:
                    logger.debug(user_info + msg)
                # if "rg" in msg_dict.keys():
                #     print("-----权限：", msg_dict["rg"])

            elif msg_dict['type'] == 'dgb':
                id = msg_dict["gfid"]
                try:
                    single_price = round(float(self.price_dict[id]) / 10, 2)
                    # print(single_price)
                    price = round(single_price * int(msg_dict['gfcnt']), 2)
                    # print(price)
                except Exception as e:
                    logger.error(
                        "{0} {1} single_price not found:{2}".format(id, self.gift_dict[id],
                                                                    str(e)))
                if id in self.gift_dict_keys:
                    # 逻辑
                    if free is False and single_price == 0.1:
                        gift_msg = self.name + "{0} 送出 {1} 个 {2} ".format(msg_dict["nn"], msg_dict["gfcnt"],
                                                                          self.gift_dict[msg_dict['gfid']])
                        # logger.debug(gift_msg)

                    else:
                        # logger.error("收到礼物")

                        timestamp = int(time.time())
                        gfid = msg_dict["gfid"]
                        gfn = self.gift_dict[gfid]
                        icon = self.pic_dic[gfid]
                        room_id = msg_dict["rid"]
                        num = msg_dict["gfcnt"]
                        if save_sql is True:
                            try:
                                sql = """
                                INSERT INTO "public"."dm" ("timestamp", "user_id", "nn", "gfid", "gfn", "icon", "room_id", "room_user", "num", "single_price", "price" )
    VALUES
        ({0}, {1}, '{2}', {3}, '{4}', '{5}', {6}, '{7}', {8}, {9}, '{10}' );
                                """.format(timestamp, msg_dict["uid"], msg_dict["nn"], gfid, gfn, icon, self.room_id,
                                           self.name,
                                           num, single_price, price)
                            except Exception as e:
                                logger.error(e)
                            try:
                                save_info(sql)
                            except Exception as e:
                                logger.error(str(e))

                        gift_msg = self.name + "{0} 送出 {1} 个 \033[1;33m{2}\033[0m ({4}) ￥{3} \n {5}".format(
                            msg_dict["nn"],
                            msg_dict["gfcnt"],
                            self.gift_dict[
                                msg_dict['gfid']],
                            price, msg_dict["gfid"],
                            self.pic_dic[
                                msg_dict["gfid"]])
                        logger.debug(gift_msg)
                        # if price > 99:
                        #     logger.error("价值连城")

                else:
                    logger.error("未知礼物！" + msg_dict["gfid"])
                    logger.debug(
                        msg_dict['nn'] + ' 送出 ' + msg_dict['gfcnt'] + '个' + msg_dict[
                            'gfid'] + "\033[1;33m {0}\033[0m".format('\t未知礼物'))

            elif msg_dict["type"] == "uenter" and int(msg_dict["nl"]) > 4:
                logger.warning(self.name + "贵族{0} {1} \033[1;35m 进入房间\033[0m".format(msg_dict["nl"], msg_dict["nn"]))

            else:
                # logger.debug(json.dumps(msg_dict).encode('utf-8').decode('unicode_escape'))
                pass

    # 发送登录信息
    def login(self):
        login_msg = 'type@=loginreq/roomid@=%s/' \
                    'dfl@=sn@AA=105@ASss@AA=0@AS@Ssn@AA=106@ASss@AA=0@AS@Ssn@AA=107@ASss@AA=0@AS@Ssn@AA=108@ASss@AA=0@AS@Ssn@AA=110@ASss@AA=0@AS@Ssn@AA=901@ASss@AA=0/' \
                    'username@=%s/uid@=%s/ltkid@=/biz@=/stk@=/devid@=8d8c22ce6093e6a7264f99da00021501/ct@=0/pt@=2/cvr@=0/tvr@=7/apd@=/rt@=1605498503/vk@=0afb8a90c2cb545e8459d60c760dc08b/' \
                    'ver@=20190610/aver@=218101901/dmbt@=chrome/dmbv@=78/' % (
                        self.room_id, self.login_name, self.login_id
                    )
        # 'visitor4444086', '1178849206'
        self.send_msg(login_msg)



    def logout(self):
        logout_msg = 'type@=logout/'
        self.send_msg(logout_msg)

    # 发送入组消息
    def join_group(self):
        join_group_msg = 'type@=joingroup/rid@=%s/gid@=-9999/' % (self.room_id)
        self.send_msg(join_group_msg)

    # 关闭礼物信息推送
    def close_gift(self):
        close_gift_msg = 'type@=dmfbdreq/dfl@=sn@AA=105@ASss@AA=1@AS@Ssn@AA=106@ASss@AA=1@AS@Ssn@AA=107@ASss@AA=1@AS@Ssn@AA=108@ASss@AA=1@AS@Ssn@AA=110@ASss@AA=1@AS@Ssn@AA=901@ASss@AA=1@AS@S/'
        self.send_msg(close_gift_msg)

    # 保持心跳线程
    def heartbeat(self):
        while True:
            # 45秒发送一个心跳包
            self.send_msg('type@=mrkl/')
            # print('debug: 发送心跳')
            time.sleep(45)

    def msg_encode(self, msg):
        # 消息以 \0 结尾，并以utf-8编码
        msg = msg + '\0'
        msg_bytes = msg.encode('utf-8')
        # 消息长度 + 头部长度8
        length_bytes = int.to_bytes(len(msg) + 8, 4, byteorder='little')
        # 斗鱼客户端发送消息类型 689
        type = 689
        type_bytes = int.to_bytes(type, 2, byteorder='little')
        # 加密字段与保留字段，默认 0 长度各 1
        end_bytes = int.to_bytes(0, 1, byteorder='little')
        # 按顺序相加  消息长度 + 消息长度 + 消息类型 + 加密字段 + 保留字段
        head_bytes = length_bytes + length_bytes + type_bytes + end_bytes + end_bytes
        # 消息头部拼接消息内容
        data = head_bytes + msg_bytes
        return data

    def msg_decode(self, msg_bytes):
        # 定义一个游标位置
        cursor = 0
        msg = []
        while cursor < len(msg_bytes):
            # 根据斗鱼协议，报文 前四位与第二个四位，都是消息长度，取前四位，转化成整型
            content_length = int.from_bytes(msg_bytes[cursor: (cursor + 4) - 1], byteorder='little')
            # 报文长度不包含前4位，从第5位开始截取消息长度的字节流，并扣除前8位的协议头，取出正文，用utf-8编码成字符串
            content = msg_bytes[(cursor + 4) + 8:(cursor + 4) + content_length - 1].decode(encoding='utf-8',
                                                                                           errors='ignore')
            msg.append(content)
            cursor = (cursor + 4) + content_length
        # print(msg)
        return msg

    def msg_format(self, msg_str):
        try:
            msg_dict = {}
            msg_list = msg_str.split('/')[0:-1]
            for msg in msg_list:
                msg = msg.replace('@s', '/').replace('@A', '@')
                msg_tmp = msg.split('@=')
                msg_dict[msg_tmp[0]] = msg_tmp[1]
            return msg_dict
        except Exception as e:
            print(str(e))

    def get_gift_dict(self):
        gift_json = {}
        gift_json1 = requests.get('https://webconf.douyucdn.cn/resource/common/gift/flash/gift_effect.json').text
        gift_json2 = requests.get(
            'https://webconf.douyucdn.cn/resource/common/prop_gift_list/prop_gift_config.json').text
        gift_json3 = requests.get("https://webconf.douyucdn.cn/resource/common/gift/gift_template/20728.json").text
        gift_json4 = requests.get("https://webconf.douyucdn.cn/resource/common/property_info_14.json").text
        # print(gift_json4.replace('DYConfigCallback(', '')[0:-2])

        gift_json1 = gift_json1.replace('DYConfigCallback(', '')[0:-2]
        gift_json2 = gift_json2.replace('DYConfigCallback(', '')[0:-2]
        gift_json3 = gift_json3.replace('DYConfigCallback(', '')[0:-2]
        gift_json1 = json.loads(gift_json1)['data']['flashConfig']
        gift_json2 = json.loads(gift_json2)['data']
        gift_json3 = json.loads(gift_json3)['data']
        for gift in gift_json1:
            gift_json[gift] = gift_json1[gift]['name']
        for gift in gift_json2:
            gift_json[gift] = gift_json2[gift]['name']
        for gift in gift_json3:
            gift_json[str(gift["id"])] = gift["name"]
        return gift_json

    def get_price_dict(self):
        price_json = {}
        pic_json = {}
        with requests.get(
                "https://webconf.douyucdn.cn/resource/common/prop_gift_list/prop_gift_config.json") as session:
            data = session.text
            data = data.replace('DYConfigCallback(', '')[0:-2]
            data = json.loads(data)["data"]
            for key, value in data.items():
                try:
                    # price_json[key] = value["pc"]
                    price_json[key] = value["exp"]
                    pic_json[key] = value["himg"]
                except:
                    print(key, "没有价格")

        with requests.get(
                "https://webconf.douyucdn.cn/resource/common/gift/gift_template/20728.json") as session:
            data = session.text
            data = data.replace('DYConfigCallback(', '')[0:-2]
            data = json.loads(data)["data"]
            for item in data:
                # price_json[item["id"]] = item["pc"]
                price_json[str(item["id"])] = item["exp"]
                pic_json[str(item["id"])] = item["himg"]
        return [price_json, pic_json]


def main(id):
    roomid = str(id)
    login_name = "visitor4444" + str(random.randint(0, 999))
    login_id = "1178849" + str(random.randint(0, 999))
    print(roomid, login_name, login_id)
    url = 'wss://danmuproxy.douyu.com:8501/'
    dy = DyDanmu(roomid, url, login_name, login_id)
    dy.start()


import threading

# thread1 = threading.Thread(target=main, args=(5645739,))
# thread2 = threading.Thread(target=main, args=(5264153,))
# thread1.start()
# thread2.start()
if __name__ == '__main__':
    for key, value in rooms.items():
        thread = threading.Thread(target=main, args=(key,))
        thread.start()
        print(thread.name)
