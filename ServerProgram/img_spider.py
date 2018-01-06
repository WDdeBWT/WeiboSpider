# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2018/01/06"

from save_to_mssql import *

import os
import re
import sys
import csv
import time
import urllib
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class SpiderWeiboImage:
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.username = ''
        self.userpass = ''
        self.url_login = 'https://passport.weibo.cn/signin/login'
        self.file_path = "F:\\Files\\weibo_taobaibai"
        self.ms_sql = MSSQL()

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

    def get_one_img(self, weibo_id, img_url):
        print("-----get_one_img, weiboid: " + str(weibo_id))
        print("img_url:" + img_url)
        try:
            self.browser.get(img_url)
            time.sleep(3)
            soup = BeautifulSoup(self.browser.page_source, "html.parser")
            img_src = soup.find_all("img")[0]["src"]
            ext = img_src.split('.')[-1]
            save_path = os.path.join(self.file_path, "image")
            save_path = os.path.join(save_path, str(weibo_id) + "_oig." + ext)
            # 保存图片数据
            data = urllib.request.urlopen(img_src).read()
            f = open(save_path, 'wb')
            f.write(data)
            f.close()
        except Exception as e:
            print(e)

    def get_all_img(self, weibo_id, img_url):
        print("-----get_all_img, weiboid: " + str(weibo_id))
        print("img_url:" + img_url)
        self.browser.get(img_url)
        time.sleep(3)
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        all_img_a = soup.find_all("a")
        i = 0
        for img_a in all_img_a:
            if "原图" in img_a.text:
                try:
                    i += 1
                    self.browser.get("http://weibo.cn" + img_a["href"])
                    time.sleep(3)
                    newsoup = BeautifulSoup(self.browser.page_source, "html.parser")
                    img_src = newsoup.find_all("img")[0]["src"]
                    ext = img_src.split('.')[-1]
                    save_path = os.path.join(self.file_path, "image")
                    save_path = os.path.join(save_path, str(weibo_id) + "_aig_" + str(i) + "." + ext)
                    # 保存图片数据
                    data = urllib.request.urlopen(img_src).read()
                    f = open(save_path, 'wb')
                    f.write(data)
                    f.close()
                except Exception as e:
                    print(e)
    
    def main(self):
        self.login_weibo()
        sql = "SELECT id, one_img_url, all_img_url FROM main_imf"
        url_list = self.ms_sql.ExecQuery(sql)
        self.ms_sql.close_connection()
        for url in url_list:
            if url[1]:
                self.get_one_img(url[0], url[1])
            elif url[2]:
                self.get_all_img(url[0], url[2])
        self.browser.close()

spide = SpiderWeiboImage()
spide.main()