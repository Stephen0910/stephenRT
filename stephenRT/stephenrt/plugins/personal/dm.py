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
import time
import requests
import json


user = "a8"
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
else:
    id = "24422"

# 一些接口可以获取是否在线等情况
# room_info = "https://www.douyu.com/roomapi/biz/getSwitch?rid={0}".format(id)
# loop_info = "https://www.douyu.com/wgapi/live/liveweb/getRoomLoopInfo?rid={0}".format(id)
# is_live = "https://www.douyu.com/wgapi/live/liveweb/roomInfo/expand?rid={0}".format(id)
# play_info = "https://www.douyu.com/lapi/live/getH5Play/{0}".format(id)
# betward = "https://www.douyu.com/betard/{0}".format(id)



class DyDanmu:
    def __init__(self, roomid, url):
        self.gift_dict = self.get_gift_dict()
        print("礼物：", self.gift_dict)
        self.gift_dict_keys = self.gift_dict.keys()
        self.room_id = roomid
        self.client = websocket.WebSocketApp(url, on_open=self.on_open, on_error=self.on_error,
                                             on_message=self.on_message, on_close=self.on_close)
        self.heartbeat_thread = threading.Thread(target=self.heartbeat)
        self.ws = None

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
            if msg_dict['type'] == 'chatmsg':
                # print("-----------", msg_dict)
                if msg_dict["bnn"] != "":
                    print("[{0}][lv{1}][{2}-lv{3}] {4}: {5}".format(msg_dict["uid"], msg_dict["level"], msg_dict["bnn"], msg_dict["bl"],  msg_dict["nn"], msg_dict["txt"]))
                else:
                    print("[{0}][lv{1}] {2}: {3}".format(msg_dict["uid"], msg_dict["level"],  msg_dict["nn"], msg_dict["txt"]))
                if "rg" in msg_dict.keys():
                    print("-----权限：", msg_dict["rg"])
                # pass
            if msg_dict['type'] == 'dgb':

                if msg_dict['gfid'] in self.gift_dict_keys:
                    print(msg_dict['nn'] + '\t送出\t' + msg_dict['gfcnt'] + '\t个\t' + self.gift_dict[msg_dict['gfid']])
                else:
                    print(msg_dict['nn'] + '\t送出\t' + msg_dict['gfcnt'] + '\t个\t' + msg_dict['gfid'] + '\t未知礼物')
                    print(msg_dict)
            if msg_dict["type"] == "uenter" and int(msg_dict["nl"]) > 3:
                print("贵族{0} {1} 进入房间".format(msg_dict["nl"], msg_dict["nn"]))


    # 发送登录信息
    def login(self):
        login_msg = 'type@=loginreq/roomid@=%s/' \
                    'dfl@=sn@AA=105@ASss@AA=0@AS@Ssn@AA=106@ASss@AA=0@AS@Ssn@AA=107@ASss@AA=0@AS@Ssn@AA=108@ASss@AA=0@AS@Ssn@AA=110@ASss@AA=0@AS@Ssn@AA=901@ASss@AA=0/' \
                    'username@=%s/uid@=%s/ltkid@=/biz@=/stk@=/devid@=8d8c22ce6093e6a7264f99da00021501/ct@=0/pt@=2/cvr@=0/tvr@=7/apd@=/rt@=1605498503/vk@=0afb8a90c2cb545e8459d60c760dc08b/' \
                    'ver@=20190610/aver@=218101901/dmbt@=chrome/dmbv@=78/' % (
                        self.room_id, 'visitor4444086', '1178849206'
                    )
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
        gift_json1 = gift_json1.replace('DYConfigCallback(', '')[0:-2]
        gift_json2 = gift_json2.replace('DYConfigCallback(', '')[0:-2]
        gift_json1 = json.loads(gift_json1)['data']['flashConfig']
        gift_json2 = json.loads(gift_json2)['data']
        for gift in gift_json1:
            gift_json[gift] = gift_json1[gift]['name']
        for gift in gift_json2:
            gift_json[gift] = gift_json2[gift]['name']
        return gift_json


if __name__ == '__main__':
    roomid = str(id)
    url = 'wss://danmuproxy.douyu.com:8501/'
    dy = DyDanmu(roomid, url)
    dy.start()


