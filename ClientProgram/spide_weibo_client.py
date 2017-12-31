# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2017/12/30"

import time

import os
import re
import sys
import socket
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


class SpiderWeiboCmt:
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.username = '15071306953'
        self.userpass = '19971027'
        self.url_login = 'https://passport.weibo.cn/signin/login'
        self.file_path = "F:\\Files\\weibo_taobaibai"

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

        for page in range(int(cmt_range/10)):
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
                    comment_text = comment.text.decode('GB2312', 'ignore').encode('utf-8')
                    print(comment_text)
                    cmt_list.append(comment_text)
                except Exception as e:
                    print(e)
        print("~~~~~~~~~~get_all_cmt END~~~~~~~~~~")
        return cmt_list


class TcpConnecter:
    def __init__(self, server_ip = '119.23.239.27', server_port = 9999):
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 建立连接:
        self.skt.connect((server_ip, server_port))
        # 接收欢迎消息:
        print(self.skt.recv(1024).decode('utf-8'))
    
    def request_cmt_url(self):
        self.skt.send(b'requestcommenturl')
        self.url_cmt = self.skt.recv(1024).decode('utf-8')
        print(self.url_cmt)
        self.id_weibo = self.skt.recv(1024).decode('utf-8')
        print(self.id_weibo)
        self.range_cmt = self.skt.recv(1024).decode('utf-8')
        print(self.range_cmt)
        print('id_weibo: ' + self.id_weibo)
        return (self.id_weibo, self.url_cmt, self.range_cmt)

    def send_cmt_list(self, list_cmt):
        print("-----send_cmt_list-----")
        for cmt in list_cmt:
            self.skt.send(bytes(cmt, encoding = "utf-8"))
        self.skt.send(b'sendcommentlistfinish')
        receipt = self.skt.recv(1024).decode('utf-8')
        if receipt == 'receiveandsavesuccess':
            self.skt.send(b'exit')
            self.skt.close()
            return '----------id_weibo:' + self.id_weibo + ' 评论数据已上传，服务端保存数据成功----------'
        else:
            return 'error: send_cmt_list'


spider = SpiderWeiboCmt()
spider.login_weibo()
tcp_conn = TcpConnecter()
id_weibo, url_cmt, range_cmt = tcp_conn.request_cmt_url()
list_cmt = spider.get_all_cmt(id_weibo, url_cmt, range_cmt)
receipt = tcp_conn.send_cmt_list(list_cmt)
print(receipt)