# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2017/12/30"

import pymssql

class MSSQL:
    """
    对pymssql的简单封装
    pymssql库，该库到这里下载：http://www.lfd.uci.edu/~gohlke/pythonlibs/#pymssql
    使用该库时，需要在Sql Server Configuration Manager里面将TCP/IP协议开启

    """

    def __init__(self):
        """
        建立连接
        得到连接信息
        返回: conn.cursor()
        """
        self.conn = pymssql.connect(host='119.23.239.27', user='WeiboSpiderUser', password='weibospideruser', database='WeiboSpiderDB', charset="utf8")
        self.cur = self.conn.cursor()
        if not self.cur:
            print("连接数据库失败")

    def ExecQuery(self,sql):
        """
        执行查询语句
        返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
        """
        self.cur.execute(sql)
        resList = self.cur.fetchall()
        return resList

    def ExecNonQuery(self,sql):
        """
        执行非查询语句
        """
        try:
            self.cur.execute(sql)
            self.conn.commit()
            self.conn.close()
            return 0
        except Exception as e:
            print(e)
            return 1
    
    def close_connection(self):
        self.conn.close()

# conn = pymssql.connect(host = '119.23.239.27', database = 'GuestBook', user = 'WeiboSpiderUser', password = 'weibospideruser')
# cur = conn.cursor()
# cur.excute("SELECT * FROM tbGuestBook")