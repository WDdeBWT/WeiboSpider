# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2017/12/30"

import time
import threading

import os
import re
import sys
import urllib
import socket
from bs4 import BeautifulSoup
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
        sock.send(b'----------Server: Connection_established----------')
        while True:
            data = sock.recv(1024)
            time.sleep(1)
            if data.decode('utf-8') == 'requestcommenturl':
                sock.send(bytes(r'http://weibo.cn/comment/E8TdzoFfm?uid=6003325152&rl=0#cmtfrm', encoding="utf-8"))
                sock.send(b'1')
                sock.send(b'100')
            if data.decode('utf-8') == 'sendcommentlistfinish':
                sock.send(b'receiveandsavesuccess')
            if not data or data.decode('utf-8') == 'exit':
                break
            print(data.decode('utf-8'))
        sock.close()
        print('Connection from %s:%s closed.' % addr)

    def main(self):
        while True:
            # 接受一个新连接:
            sock, addr = self.skt.accept()
            # 创建新线程来处理TCP连接:
            t = threading.Thread(target=self.tcplink, args=(sock, addr))
            t.start()


test1 = Test()
test1.main()
