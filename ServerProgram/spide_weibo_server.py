# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2017/12/30"

from save_to_mssql import *

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
    
    def get_main_ifmt(self):
        pages = 10
        cmt_range = 30000
        try:
            for i in range(pages):
                url_index = 'https://weibo.cn/u/6003325152?filter=1'
                url_index = url_index + "&page=" + str(i+1)
                print("--------------------page:" + str(i+1) + "--------------------")
                print(url_index)

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
                        cmt_str = ""
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
                                if cmt_count > cmt_range:
                                    mimf.cmt_finish = 1
                                else:
                                    mimf.comment_url = one_a["href"]
                            if "赞" in one_a.text:
                                pattern = re.compile('\[(.*?)\]')
                                like_count = int(re.findall(pattern, one_a.text)[0])
                                mimf.like_count = like_count
                        mimf.insert_data()
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)
        print("-------------------- get_main_ifmt 运行结束，当前时间：" + str(time.strftime('%Y-%m-%d',time.localtime(time.time()))) + "--------------------")


class MainImf:
    def __init__(self, weibo_content = '', weibo_time = '2000-1-1', comment_url = '', one_img_url = '', all_img_url = '', comment_count = 0, like_count = 0, img_finish = 0, cmt_finish = 0):
        self.weibo_content = weibo_content
        self.weibo_time = weibo_time
        self.comment_url = comment_url
        self.one_img_url = one_img_url
        self.all_img_url = all_img_url
        self.comment_count = comment_count
        self.like_count = like_count
        self.img_finish = img_finish
        self.cmt_finish = cmt_finish
        self.ms_sql = MSSQL()
    
    def insert_data(self):
        sql = "INSERT INTO main_imf VALUES('" + self.weibo_content + "', '" + self.weibo_time + "', '" + self.comment_url + "', '" + self.one_img_url + "', '" + self.all_img_url + "', " + str(self.comment_count) + ", " + str(self.like_count) + ", " + str(self.img_finish) + ", " + str(self.cmt_finish) + ")"
        if 1 == self.ms_sql.ExecNonQuery(sql):
            print("----------保存到数据库失败，微博内容：" + self.weibo_content + "----------")


spider = SpiderWeiboMainImf()
spider.login_weibo()
spider.get_main_ifmt()
