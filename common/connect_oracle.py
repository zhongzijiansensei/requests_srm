import cx_Oracle
from common.readconfig import ReadConfig
#
#
#
#
#
# class DbConnect():
#     def __init__(self):
#         # 打开数据库
#         self.db = cx_Oracle.connect(user, password, host)
#         # 使用cursor()方式获取操作游标
#         self.cursor = self.db.cursor()
#
#     def select(self, sql):
#         # sql查询
#         self.cursor.execute(sql)  # 执行sql
#         results = self.cursor.fetchall()
#         return results
#
#     def execute(self, sql):
#         # sql 删除 提示 修改
#         try:
#             self.cursor.execute(sql)  # 执行sql
#             self.db.commit()  # 提交修改
#         except:
#             # 发生错误时回滚
#             self.db.rollback()
#
#     def close(self):
#         self.db.close()  # 关闭连接
#
#
# def select_sql(select_sql):
#     '''查询数据库'''
#     db = DbConnect(user1, password1, host1)
#     result = db.select(select_sql)
#     db.close()
#     return result
#
#
# def execute_sql(sql):
#     '''执行SQL'''
#     db = DbConnect(user, password, host)
#     db.execute(sql)
#     db.close()
#
#
# if __name__ == '__main__':
#     user1 = ReadConfig().get_cx('user')
#     password1 = ReadConfig().get_cx('password')
#     host = ReadConfig().get_cx('host')
#     sql = 'select * from SYS_USER WHERE PHONE = 15555555551'
#     delete = select_sql(sql)
#     print(delete)
class OracleOperation(object):

    # 执行下面的execute_sql方法时会自动执行该初始化方法进行连接数据库
    def __init__(self):
        # 建立连接
        self.conn = cx_Oracle.connect("srmuat", "Qy_srmuat" , "172.30.3.232:1521/srmtest")
        # 创建游标
        self.cursor = self.conn.cursor()

    def execute_sql(self, sql):
        """
        执行sql语句，并commit提交
        :param sql:需要执行的sql语句
        :return:
        """
        self.cursor.execute(sql)
        self.conn.commit()

    def get_data(self):
        """
        获得查询数据
        :return: 返回查到的数据
        """
        data = self.cursor.fetchall()
        return data

    def close_oracle(self):
        # 关闭游标
        self.cursor.close()
        # 关闭数据库连接
        self.conn.close()

if __name__ == '__main__':
    sql = 'select * from SYS_USER WHERE PHONE = 15555555551'
    delete = OracleOperation().execute_sql(sql)