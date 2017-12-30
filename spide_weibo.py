# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2017/12/06"

import time

from lxml import etree

import os
import re
import sys
import csv
import urllib
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class SpiderWeibo:
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


    def get_main_ifmt(self):
        pages = 52
        weibo_id = 0
        cmt_range = 20000
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
                        weibo_id += 1
                        print("--------------------weibo_id:" + str(weibo_id) + "--------------------")
                        content = result.find_all("span", class_="ctt")[0].text
                        print("content:" + content)
                        cmt_str = ""
                        all_a = result.find_all("a")
                        # get url_img and url_cmt
                        flag = 0
                        for one_a in all_a:
                            if "组图" in one_a.text:
                                flag = 1
                                self.get_all_img(weibo_id, one_a["href"])
                            if "原图" in one_a.text:
                                if flag == 1:
                                    continue
                                self.get_one_img(weibo_id, one_a["href"])
                            if "评论" in one_a.text:
                                pattern = re.compile('\[(.*?)\]')
                                num_weibo = int(re.findall(pattern, one_a.text)[0])
                                if num_weibo > cmt_range:
                                    cmt_str = "Out of range"
                                else:
                                    url_cmt = one_a["href"]
                                    cmt_str = self.get_all_cmt(weibo_id, url_cmt, cmt_range)
                        save_path = os.path.join(self.file_path, "string")
                        save_path_1 = os.path.join(save_path, str(weibo_id) + "_ctt.txt")
                        save_path_2 = os.path.join(save_path, str(weibo_id) + "_cmt.txt")

                        f_1 = open(save_path_1, 'w', encoding='utf-8')
                        f_1.write(content)
                        f_1.close()

                        f_2 = open(save_path_2, 'w', encoding='utf-8')
                        f_2.write(cmt_str)
                        f_2.close()
                        # temp sleep
                        # time.sleep(1)
                    except Exception as e:
                        print(e)
        except Exception as e:
            print(e)
        print("--------------------运行结束，当前时间：" + str(time.strftime('%Y-%m-%d',time.localtime(time.time()))) + "--------------------")

    def get_one_img(self, weibo_id, img_url):
        print("**********get_one_img**********")
        print("img_url:" + img_url)
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
        print("**********get_one_img END**********")

    def get_all_img(self, weibo_id, img_url):
        print("**********get_all_img**********")
        print("img_url:" + img_url)
        self.browser.get(img_url)
        time.sleep(3)
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        all_img_a = soup.find_all("a")
        i = 0
        for img_a in all_img_a:
            if "原图" in img_a.text:
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
        print("**********get_all_img END**********")

    def get_all_cmt(self, weibo_id, cmt_url, range_cmt):
        print("~~~~~~~~~~get_all_cmt~~~~~~~~~~")
        cmt_str = ""

        if "#cmtfrm" in cmt_url:
            cmt_url = cmt_url[:-7]
        print("cmt_url:" + cmt_url)

        for page in range(int(range_cmt/10)):
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
                    comment = div_cmt.find_all("span", class_="ctt")[0]
                    print(comment.text)
                    cmt_str = cmt_str + comment.text + "；"
                except Exception as e:
                    print(e)
        print("~~~~~~~~~~get_all_cmt END~~~~~~~~~~")
        return cmt_str


spider = SpiderWeibo()
spider.login_weibo()
#spider.spide_base_message()
#spider.spide_weibo_messge()
spider.get_main_ifmt()
