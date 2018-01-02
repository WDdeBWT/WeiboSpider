# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2017/12/30"

s = set()
s.add(2)
print(s)
s.add(2)
print(s)
s.remove(2)
print(s)
if 3 in s:
    s.remove(3)
else:
    print("not in")
print(s)
print("--1-1--")
