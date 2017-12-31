# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2017/12/31"

import os
import re
import sys
import time
import urllib
import socket
import struct
import threading
from bs4 import BeautifulSoup
from multiprocessing import Queue
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


class Test:
    def __init__(self):
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.skt.bind(('0.0.0.0', 9999))
        self.skt.listen(10)
        print('Waiting for connection...')

    def tcplink(self, sock, addr):
        print('Accept new connection from %s:%s...' % addr)
        self.send_bag(sock, '----------Server: Connection_established----------', 1)
        while True:
            data = sock.recv(1024)
            body = data[8:]
            time.sleep(1)
            if body.decode('utf-8', 'ignore') == 'requestcommenturl':
                self.send_bag(sock, r'http://weibo.cn/comment/E8TdzoFfm?uid=6003325152&rl=0#cmtfrm', 3)
                self.send_bag(sock, '1', 3)
                self.send_bag(sock, '100', 3)
            if body.decode('utf-8', 'ignore') == 'sendcommentlistfinish':
                self.send_bag(sock, 'receiveandsavesuccess', 2)
            if not body or body.decode('utf-8', 'ignore') == 'exit':
                break
            print(body.decode('utf-8', 'ignore'))
        sock.close()
        print('Connection from %s:%s closed.' % addr)

    def send_bag(self, sock, data, data_type):
        body = bytes(data, encoding = "utf-8")
        # print(body)
        header = [body.__len__(), data_type]
        head_pack = struct.pack("!2I", *header)
        sock.send(head_pack + body)
    
    def main(self):
        while True:
            # 接受一个新连接:
            sock, addr = self.skt.accept()
            # 创建新线程来处理TCP连接:
            t = threading.Thread(target=self.tcplink, args=(sock, addr))
            t.start()


test1 = Test()
test1.main()
