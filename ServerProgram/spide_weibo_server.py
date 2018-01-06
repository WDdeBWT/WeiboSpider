# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2017/12/30"

from database_model import *

import os
import re
import sys
import time
import urllib
import socket
import struct
import threading
from datetime import datetime 
from bs4 import BeautifulSoup
from multiprocessing import Queue
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


class SpiderWeiboMainImf:
    def __init__(self, pages, cmt_range, q_sql):
        self.browser = webdriver.Chrome()
        self.username = ''
        self.userpass = ''
        self.url_login = 'https://passport.weibo.cn/signin/login'
        self.pages = pages
        self.cmt_range = cmt_range
        self.q_sql = q_sql

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
    
    def get_main_ifmt(self):
        try:
            for i in range(self.pages):
                url_index = 'https://weibo.cn/u/6003325152?filter=1'
                url_index = url_index + "&page=" + str(i+1)
                print("--------------------get_main_ifmt, page:" + str(i+1) + "--------------------")
                # print(url_index)

                # collect the weibo in this page
                self.browser.get(url_index)
                time.sleep(3)
                soup = BeautifulSoup(self.browser.page_source, "html.parser")

                results = soup.find_all("div", class_="c")
                if not results:
                    continue
                for result in results:
                    try:
                        if not result.find_all("span", class_="ctt"):
                            continue
                        # search the content
                        mimf = MainImf()
                        content = result.find_all("span", class_="ctt")[0].text
                        mimf.weibo_content = content
                        # print("content:" + content)
                        all_a = result.find_all("a")
                        # get url_img and url_cmt
                        flag = 0
                        for one_a in all_a:
                            if "组图" in one_a.text:
                                flag = 1
                                mimf.all_img_url = one_a["href"]
                            if "原图" in one_a.text:
                                if flag == 1:
                                    continue
                                mimf.one_img_url = one_a["href"]
                            if "评论" in one_a.text:
                                pattern = re.compile('\[(.*?)\]')
                                cmt_count = int(re.findall(pattern, one_a.text)[0])
                                mimf.comment_count = cmt_count
                                if cmt_count > self.cmt_range:
                                    mimf.cmt_finish = 1
                                else:
                                    mimf.comment_url = one_a["href"]
                            if "赞" in one_a.text:
                                pattern = re.compile('\[(.*?)\]')
                                like_count = int(re.findall(pattern, one_a.text)[0])
                                mimf.like_count = like_count
                        self.q_sql.put(mimf.insert_data())
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)
        self.browser.close()
        print("-------------------- get_main_ifmt 运行结束，当前时间：" + str(time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))) + "--------------------")