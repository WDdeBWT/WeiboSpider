# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2017/12/31"

import time
import socket
import struct
import threading
from multiprocessing import Queue


class TcpConnecter(threading.Thread):
    """
    TcpConnecter接收数据的双层循环，按照自定义应用层协议的规则
    """
    def __init__(self, q_recv, server_ip, server_port):
        threading.Thread.__init__(self)
        self.q_recv = q_recv
        self.server_ip = server_ip
        self.server_port = server_port

    def run(self):
        data_buffer = bytes()
        header_size = 8
        # 建立连接:
        self.skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.skt.connect((self.server_ip, self.server_port))
        # 双层循环，从自定义的应用层协议中取出格式化的数据
        while True:
            data = self.skt.recv(1024)
            if data:
                # 把数据存入缓冲区，类似于push数据
                data_buffer += data
                while True:
                    if len(data_buffer) < header_size:
                        # print("数据包（%s Byte）小于消息头部长度，跳出小循环" % len(data_buffer))
                        break
                    # 读取包头
                    # struct中:!代表Network order，2i代表2个int数据
                    head_pack = struct.unpack('!2i', data_buffer[:header_size])
                    body_size = head_pack[0]
                    # 分包情况处理，跳出函数继续接收数据
                    if len(data_buffer) < header_size + body_size:
                        # print("数据包（%s Byte）不完整（总共%s Byte），跳出小循环" % (len(data_buffer), header_size + body_size))
                        break
                    # 读取消息正文的内容
                    body = data_buffer[header_size:header_size + body_size]
                    # 将数据类型和数据主体放入q_recv队列中，设置阻塞超时为1s（理论上客户端不允许超时）
                    self.q_recv.put((head_pack[1], body.decode('utf-8')), block=True, timeout=1)
                    # 获取下一个数据包，类似于把数据pop出（粘包情况的处理）
                    data_buffer = data_buffer[header_size + body_size:]
    
    def send_bag(self, data, data_type):
        if type(data) != bytes:
            body = bytes(data, encoding = "utf-8")
        header = [body.__len__(), data_type]
        head_pack = struct.pack("!2I", *header)
        self.skt.send(head_pack + body)





















