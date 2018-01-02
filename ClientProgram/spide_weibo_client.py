# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2017/12/30"

from TCP_connecter import *

import os
import re
import sys
import time
import socket
from bs4 import BeautifulSoup
from multiprocessing import Queue
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


class SpiderWeiboCmt:
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.username = '15071306953'
        self.userpass = '19971027'
        self.url_login = 'https://passport.weibo.cn/signin/login'

    def login_weibo(self):
        self.browser.get(self.url_login)

        time.sleep(3)
        elem_user = self.browser.find_element_by_id('loginName')
        elem_pass = self.browser.find_element_by_id('loginPassword')

        elem_user.send_keys(self.username)
        elem_pass.send_keys(self.userpass)

        time.sleep(2)

        elem_pass.send_keys(Keys.RETURN)
        time.sleep(8)

        print("--------------------login success--------------------")
    
    def get_all_cmt(self, weibo_id, cmt_url, cmt_range):
        print("~~~~~~~~~~get_all_cmt~~~~~~~~~~")
        cmt_list = []

        if "#cmtfrm" in cmt_url:
            cmt_url = cmt_url[:-7]
        print("cmt_url:" + cmt_url)

        for page in range(int(int(cmt_range)/10)):
            crt_url = cmt_url + "&page=" + str(page+1) # current_page_url
            self.browser.get(crt_url)
            time.sleep(3)
            print("----------Commtent page:" + str(page+1) + "----------")
            # 查找该页面所有评论的div
            soup = BeautifulSoup(self.browser.page_source, "html.parser")
            all_div_cmt = soup.find_all("div", class_ = 'c', id = re.compile("^C_"))
            # 如果本页没有评论，则跳出翻页循环
            if not all_div_cmt:
                print("本页无内容")
                break
            # 遍历评论
            for div_cmt in all_div_cmt:
                try:
                    # 取出评论内容，添加到cmt_list中
                    comment = div_cmt.find_all("span", class_="ctt")[0]
                    comment_text = comment.text
                    print(comment_text)
                    cmt_list.append(comment_text)
                except Exception as e:
                    print(e)
        print("~~~~~~~~~~get_all_cmt END~~~~~~~~~~")
        return cmt_list


class ConnectingBridge:
    def __init__(self, server_ip = '119.23.239.27', server_port = 9999):
        self.q_recv = Queue(maxsize = 10)
        self.tcp_conn = TcpConnecter(self.q_recv, server_ip, server_port)
        self.tcp_conn.start()
        try:
            recv = self.q_recv.get(block=True, timeout=10)
            if recv[0] == 1:
                print(recv[1])
            else:
                print("error 1")
                os.system('pause')
                sys.exit(1)
        except Exception as e:
            print(e)
            print("----------连接服务器失败1，请关闭程序，稍后再试----------")
            self.tcp_conn.end_thread()
            os.system('pause')
            sys.exit(1)
        
    
    def request_cmt_url(self):
        self.tcp_conn.send_bag('requestcommenturl', 2)
        try:
            recv = self.q_recv.get(block=True, timeout=10)
            if (recv[0] == 2) and (recv[1] == 'finishcatchingweibo'):
                print('----------爬取任务已全部完成，感谢您的帮助，再见----------')
                return (0, 0, 0)
            self.id_weibo = recv[1]
            self.url_cmt = self.q_recv.get(block=True, timeout=10)[1]            
            self.range_cmt = self.q_recv.get(block=True, timeout=10)[1]
            print('-----id_weibo: ' + self.id_weibo + " range_cmt: " + self.range_cmt + "-----")
            return (self.id_weibo, self.url_cmt, self.range_cmt)
        except Exception as e:
            print(e)
            print("----------连接服务器失败2，请关闭程序，稍后再试----------")
            self.tcp_conn.end_thread()
            os.system('pause')
            sys.exit(1)

    def send_cmt_list(self, list_cmt):
        print("-----send_cmt_list-----")
        try:
            for cmt in list_cmt:
                self.tcp_conn.send_bag(cmt, 3)
            self.tcp_conn.send_bag('sendcommentlistfinish', 2)
            recv = self.q_recv.get(block=True, timeout=300)
            if (recv[0] == 2) and (recv[1] == 'receiveandsavesuccess'):
                print('----------id_weibo:' + self.id_weibo + ' 评论数据已上传，服务端保存数据成功----------')
                self.tcp_conn.send_bag('exittcplink', 2)
                self.tcp_conn.end_thread()
                return 0
            else:
                print("error 2")
                self.tcp_conn.end_thread()
                os.system('pause')
                sys.exit(1)
        except Exception as e:
            print(e)
            print("----------连接服务器失败3，请关闭程序，稍后再试----------")
            self.tcp_conn.end_thread()
            os.system('pause')
            sys.exit(1)


spider = SpiderWeiboCmt()
spider.login_weibo()
for i in range(100):
    print("----------本客户端正在进行第" + (i+1) + "次微博评论爬取工作（每次大约需要30-90分钟）----------")
    tcp_conn_brdg = ConnectingBridge()
    id_weibo, url_cmt, range_cmt = tcp_conn_brdg.request_cmt_url()
    if not (id_weibo == 0):
        list_cmt = spider.get_all_cmt(id_weibo, url_cmt, range_cmt)
        receipt = tcp_conn_brdg.send_cmt_list(list_cmt)
        if receipt == 0:
            print("----------爬取完成，weibo_id: " + id_weibo + "----------")
            print(" ")