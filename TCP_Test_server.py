# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2017/12/30"

import time
import threading

import socket

def test1():
    while True:
        print("-----")
        time.sleep(3)

def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcome!')
    t = threading.Thread(target=test1, args=())
    t.start()
    while True:
        try:    
            data = sock.recv(1024)
        except Exception as e:
            print("---11--")
            break
        time.sleep(1)
        # if not data or data.decode('utf-8') == 'exit':
        if not data:
            break
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    if sock:
        print(sock)
        print(data)
        print("true")
    else:
        print("false")
    sock.close()
    print('Connection from %s:%s closed.' % addr)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 监听端口:
s.bind(('127.0.0.1', 9999))
# 等待数量设置为5
s.listen(5)
print('Waiting for connection...')

while True:
    # 接受一个新连接:
    sock, addr = s.accept()
    # 创建新线程来处理TCP连接:
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()