import pymysql
from common.readconfig import ReadConfig

# dbinfo = {
#     "host": "172.30.3.232",
#     "user": "srmuat",
#     "password": "Qy_srmuat",
#     "port": 1521
# }

dbinfo = eval(ReadConfig().get_db("dbinfo"))
# pymysql.connect('172.30.3.232','srmuat','Qy_srmuat', 1521)
class DbConnect():
    def __init__(self, db_conf, database=""):
        self.db_conf = db_conf
        # 打开数据库
        self.db = pymysql.connect(database=database,
                                  cursorclass=pymysql.cursors.DictCursor,
                                  **db_conf)
        # 使用cursor()方式获取操作游标
        self.cursor = self.db.cursor()

    def select(self, sql):
        # sql查询
        self.cursor.execute(sql)  # 执行sql
        results = self.cursor.fetchall()
        return results
#
    def execute(self, sql):
        # sql 删除 提示 修改
        try:
            self.cursor.execute(sql)  # 执行sql
            self.db.commit()  # 提交修改
        except:
            # 发生错误时回滚
            self.db.rollback()

    def close(self):
        self.db.close()  # 关闭连接

#
def select_sql(select_sql):
    '''查询数据库'''
    db = DbConnect(dbinfo, database='srmtest')
    result = db.select(select_sql)
    db.close()
    return result


def execute_sql(sql):
    '''执行SQL'''
    db = DbConnect(dbinfo, database='srmtest')
    db.execute(sql)
    db.close()


if __name__ == '__main__':
    sql = 'delete from SYS_USER WHERE PHONE = 15555555551'
    delete = execute_sql(sql)
    print(delete)
