# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2017/12/31"

from auto_sql import *
from database_model import *
from spide_weibo_server import *
from TCP_connecter_server import *

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


class CommanderServer:
    def __init__(self):
        self.q_sql = Queue(maxsize = 0)
        self.range_cmt = 30000
        self.pages = 60
        self.is_catching = set()
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.skt.bind(('0.0.0.0', 9999))
        self.skt.listen(10)
        print('Waiting for connection...')

    def tcp_link(self, sock, addr, weibo_id, cmt_range, cmt_url):
        cmt_list = [] # comment list
        ist_order = 0 # insert order
        q_recv = Queue(maxsize = self.range_cmt + 10)
        tcp_conn = TcpConnecterServer(q_recv, sock)
        tcp_conn.start()
        print('Accept new connection from %s:%s...' % addr)
        print("^TIME^: " + str(time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))))
        tcp_conn.send_bag('----------Server: Connection_established----------', 1)

        while True:
            try:
                recv = q_recv.get(block=True, timeout=14400)
            except Exception as e:
                print('Lost connection from%s:%s...' % addr)
                print("^TIME^: " + str(time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))))
                break
            if (recv[0] == 2) and (recv[1] == 'requestcommenturl'):# 收到爬取请求，发送相关数据
                if weibo_id == 0:# 如果weibo_id == 0即爬取全部完成，则发送结束信号
                    tcp_conn.send_bag('finishcatchingweibo', 2)
                    break
                tcp_conn.send_bag(str(weibo_id), 3)
                tcp_conn.send_bag(cmt_url, 3)
                tcp_conn.send_bag(str(cmt_range), 3)

            elif recv[0] == 3:# 收到数据，添加到cmt_list中
                ist_order += 1
                cmt_list.append((recv[1], ist_order))

            elif (recv[0] == 2) and (recv[1] == 'sendcommentlistfinish'):# 收到数据发送完毕指令，开始保存数据
                print("-----Saving to database, weibo_id: " + str(weibo_id) + "-----")
                print("^TIME^: " + str(time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))))
                cimf = CmtImf(weibo_id, '')
                for cmt in cmt_list:
                    cimf.weibo_comment = cmt[0]
                    cimf.insert_order = cmt[1]
                    # cimf.insert_data()
                    self.q_sql.put(cimf.insert_data())
                # cimf.close()
                mimf = MainImf()
                # mimf.update_data(weibo_id, "cmt_finish", 1)
                self.q_sql.put(mimf.update_data(weibo_id, "cmt_finish", 1))
                # mimf.close()
                tcp_conn.send_bag('receiveandsavesuccess', 2)
                print("-----Receive and save success, weibo_id: " + str(weibo_id) + "-----")
                print("^TIME^: " + str(time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))))

            elif (recv[0] == 2) and (recv[1] == 'exittcplink'):# 收到关闭连接指令，关闭连接
                break
            # print(recv[1])
        try:
            tcp_conn.end_thread()
            time.sleep(1)
            sock.close()
        except Exception as e:
            print(e)
            print("^TIME^: " + str(time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))))
        print('Connection from %s:%s closed.' % addr)
        print("^TIME^: " + str(time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))))
        if weibo_id in self.is_catching:
            self.is_catching.remove(weibo_id)
        return 0

    def commander(self):
        print("----------分布式微博爬虫服务端程序----------")
        print("^TIME^: " + str(time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))))
        au_svr = AutoSql(self.q_sql)
        au_svr.start()

        ip_list = []

        # 执行SpiderWeiboMainImf，爬取全部微博主体信息
        spider = SpiderWeiboMainImf(self.pages, self.range_cmt, self.q_sql)
        spider.login_weibo()
        spider.get_main_ifmt()

        while True:
            flag = 0
            # 接受一个新连接:
            sock, addr = self.skt.accept()
            # 判断ip是否合法
            if addr[0] not in ip_list:
                sock.close()
                print('Refuse new connection from %s:%s...' % addr)
                print("^TIME^: " + str(time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))))
                continue
            # 从数据库中找到需要爬取的url_cmt，创建新线程来处理TCP连接:
            mimf = MainImf()
            # results = mimf.select_data()
            # mimf.close()
            results = au_svr.select_db(mimf.select_data())
            for result in results:
                if (result[9] == False) and (result[0] not in self.is_catching):
                    flag = 1
                    self.is_catching.add(result[0])
                    t = threading.Thread(target=self.tcp_link, args=(sock, addr, result[0], self.range_cmt, result[3]))
                    t.start()
                    break
            if flag == 0:
                t = threading.Thread(target=self.tcp_link, args=(sock, addr, 0, 0, ''))
                t.start()
            # 每添加一个新连接之后，打印现在全部正在爬取的连接对应的weibo_id
            print("-----set: is_catching: " + str(self.is_catching) + ", present time: " + str(time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))) + "-----")

cmd_server = CommanderServer()
cmd_server.commander()
