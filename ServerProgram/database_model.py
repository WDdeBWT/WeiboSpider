# _*_ coding:utf-8 _*_
__author__ = "WDdeBWT"
__date__ = "2018/01/02"


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
        # self.ms_sql = MSSQL()
    
    def insert_data(self):
        sql = "INSERT INTO main_imf VALUES('" + self.weibo_content + "', '" + self.weibo_time + "', '" + self.comment_url + "', '" + self.one_img_url + "', '" + self.all_img_url + "', " + str(self.comment_count) + ", " + str(self.like_count) + ", " + str(self.img_finish) + ", " + str(self.cmt_finish) + ")"
        return (2, sql)
        # if 1 == self.ms_sql.ExecNonQuery(sql):
        #     print("---------- MainImf 保存到数据库失败，微博内容：" + self.weibo_content + "----------")
    
    def update_data(self, weibo_id, update_item, update_value):
        sql = "UPDATE main_imf SET " + update_item + " = " + str(update_value) + " WHERE id = " + str(weibo_id)
        return (2, sql)
        # if 1 == self.ms_sql.ExecNonQuery(sql):
        #     print("---------- MainImf 更新到数据库失败，微博内容：" + self.weibo_content + "----------")
    
    def select_data(self):
        sql = "SELECT * FROM main_imf"
        return (1, sql)
        # return self.ms_sql.ExecQuery(sql)
    
    # def close(self):
    #     self.ms_sql.close_connection()


class CmtImf:
    def __init__(self, weibo_id = 0, weibo_comment = ''):
        self.weibo_id = weibo_id
        self.weibo_comment = weibo_comment
        # self.ms_sql = MSSQL()
    
    def insert_data(self):
        sql = "INSERT INTO cmt_imf VALUES(" + str(self.weibo_id) + ", '" + self.weibo_comment + "')"
        return (2, sql)
        # if 1 == self.ms_sql.ExecNonQuery(sql):
        #     print("---------- CmtImf 保存到数据库失败，weibo_id：" + str(self.weibo_id) + "----------")

    def select_data(self):
        sql = "SELECT * FROM cmt_imf"
        return (1, sql)
        # return self.ms_sql.ExecQuery(sql)
    
    # def close(self):
    #     self.ms_sql.close_connection()


class ImgImf:
    def __init__(self, weibo_id = 0, img_path = ''):
        self.weibo_id = weibo_id
        self.img_path = img_path
        # self.ms_sql = MSSQL()
    
    def insert_data(self):
        sql = "INSERT INTO img_imf VALUES(" + str(self.weibo_id) + ", '" + self.img_path + "')"
        return (2, sql)
        # if 1 == self.ms_sql.ExecNonQuery(sql):
        #     print("---------- ImgImf 保存到数据库失败，weibo_id：" + str(self.weibo_id) + "----------")

    def select_data(self):
        sql = "SELECT * FROM img_imf"
        return (1, sql)
        # return self.ms_sql.ExecQuery(sql)
    
    # def close(self):
    #     self.ms_sql.close_connection()