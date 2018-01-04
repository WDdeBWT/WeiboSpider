# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2018/01/02"

import time
import threading
from multiprocessing import Queue

from save_to_mssql import *


class SqlServer(threading.Thread):
    def __init__(self, q_sql):
        threading.Thread.__init__(self)
        self.q_sql = q_sql
        self.ms_sql = MSSQL()
    
    def run(self):
        while True:
            time.sleep(0.02)
            data = self.q_sql.get()
            if data[0] == 1:
                return self.ms_sql.ExecQuery(data[1])
            if data[0] == 2:
                self.ms_sql.ExecNonQuery(data[1])