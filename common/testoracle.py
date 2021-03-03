import json
import os
import cx_Oracle
from common.json_rewrite import DateEncoder

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
"""python version 3.7"""


class TestOracle(object):
    def __init__(self, user, pwd, ip, port, sid):
        self.connect = cx_Oracle.connect(user + "/" + pwd + "@" + ip + ":" + port + "/" + sid)
        self.cursor = self.connect.cursor()

    def select(self, sql):
        li = []
        self.cursor.execute(sql)
        result = self.cursor.fetchall()  # 返回元组
        col_name = self.cursor.description
        for row in result:
            di = {}
            for col in range(len(col_name)):
                key = col_name[col][0]
                value = row[col]
                di[key] = value
            li.append(di)
        data = json.dumps(li, cls=DateEncoder, ensure_ascii=False, indent=2, separators=(',', ':'))
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
            print("delete ok")
        except Exception as e:
            print(e)
        finally:
            self.disconnect()


if __name__ == "__main__":
    # test_oracle = TestOracle('srmuat', 'Qy_srmuat', '172.30.3.232', '1521', 'srmtest')
    param = [('ww1', 'job003', 1333, 2), ('ss1', 'job004', 1444, 2)]
    # test_oracle.insert("insert into bonus(ENAME,JOB,SAL,COMM)values(:1,:2,:3,:4)",param)#也可以下面这样解决orc-1036非法变量问题
    # test_oracle.insert("insert into bonus(ENAME,JOB,SAL,COMM)values (:ENAME,:JOB,:SAL,:COMM)", param)
    # test_oracle1 = TestOracle('SCOTT', 'pipeline', '127.0.0.1', '1521', 'orcl')
    # test_oracle1.delete("delete from bonus where ENAME='ss1' or ENAME='ww1'")
    test_oracle3 = TestOracle('srmuat', 'Qy_srmuat', '172.30.3.232', '1521', 'srmtest')
    js = test_oracle3.select("select * from SYS_USER WHERE PHONE like '155%'")
    print(js)