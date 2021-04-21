import json
import os
import cx_Oracle
from common.json_rewrite import DateEncoder
from common.readconfig import ReadConfig
#
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'



class Db_Oracle(object):
    def __init__(self):
        user = ReadConfig().get_cx('user')
        pwd = ReadConfig().get_cx('pwd')
        ip = ReadConfig().get_cx('ip')
        host = ReadConfig().get_cx('host')
        sid = ReadConfig().get_cx('sid')
        self.connect = cx_Oracle.connect(user + "/" + pwd + "@" + ip + ":" + host + "/" + sid)
        self.cursor = self.connect.cursor()

    def select(self, sql):
        # li = []
        self.cursor.execute(sql)
        result = self.cursor.fetchall()  # 返回所有列的值
        col_name = self.cursor.description   # 获取列名
        for row in result:
            di = {}
            for col in range(len(col_name)):
                key = col_name[col][0]
                value = row[col]
                di[key] = value
            # li.append(di)
        str_data = json.dumps(di, cls=DateEncoder, ensure_ascii=False, indent=2, separators=(',', ':'))
        data = json.loads(str_data)

        return data

    def disconnect(self):
        self.cursor.close()
        self.connect.close()

    def insert(self, sql, list_param):
        try:
            self.cursor.executemany(sql, list_param)
            self.connect.commit()
            print("插入ok")
        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    def update(self, sql):
        try:
            self.cursor.execute(sql)
            self.connect.commit()

        except Exception as e:
            print(e)
        finally:
            self.disconnect()

    def delete(self, sql):
        try:
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception as e:
            print(e)
        finally:
            self.disconnect()


if __name__ == "__main__":
    # test_oracle = TestOracle('srmuat', 'Qy_srmuat', '172.30.3.232', '1521', 'srmtest')
    # test_oracle.insert("insert into bonus(ENAME,JOB,SAL,COMM)values(:1,:2,:3,:4)",param)#也可以下面这样解决orc-1036非法变量问题
    # test_oracle.insert("insert into bonus(ENAME,JOB,SAL,COMM)values (:ENAME,:JOB,:SAL,:COMM)", param)
    # test_oracle3 = TestOracle('srmuat', 'Qy_srmuat', '172.30.3.232', '1521', 'srmtest')
    sql = "select * FROM SYS_USER WHERE PHONE = '15555555551'"
    js = Db_Oracle().select(sql)
    # js = TestOracle().select("select * from SYS_USER WHERE PHONE like '155%'")
    print(js)
    print(type(js))
