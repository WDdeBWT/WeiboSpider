# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2018/01/02"

import time
import threading
from multiprocessing import Queue

from save_to_mssql import *


class AutoSql(threading.Thread):
    """
    自动按照q_sql队列执行sql代码，降低数据库压力，提高数据库可靠性
    """
    def __init__(self, q_sql):
        threading.Thread.__init__(self)
        self.q_sql = q_sql
        self.ms_sql = MSSQL()
    
    def run(self):
        while True:
            time.sleep(0.01)
            sql = self.q_sql.get()
            self.ms_sql.ExecNonQuery(sql)
    
    def select_db(self, sql):
        i = 0
        while not self.q_sql.empty():
            time.sleep(10)
            i += 1
            if i%10 == 0:
                print("WARNING: q_sql is not empty, times: " + str(i/10) + ", present time: " + str(time.strftime('%m-%d %H:%M:%S',time.localtime(time.time()))))
        return self.ms_sql.ExecQuery(sql)