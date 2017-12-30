# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2017/12/30"

import requests

url = r'https://weibo.cn/comment/FC1Nwh25C?uid=6003325152&rl=0&page=1'
r = requests.get(url)
print(r.encoding)
print(r.apparent_encoding)