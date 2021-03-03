import cx_Oracle

conn = cx_Oracle.connect("srmuat", "Qy_srmuat" , "172.30.3.232:1521/srmtest") #用自己的实际数据库用户名、密码、主机ip地址 替换即可

curs=conn.cursor()

sql='select * from SYS_USER WHERE PHONE = 15555555551'

rr=curs.execute (sql)

row=curs.fetchone()

print(row[1])

curs.close()
