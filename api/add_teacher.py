'''
Code description：显示老师
Create time：
Developer：
'''
import os

import requests
import rerere
from requests_toolbelt import MultipartEncoder
from api.login_xadmin import Login_Admin

class Add_Teacher():

    def __init__(self,s:requests.session):
        self.s = s

    def add_teacher(self,teacher_name="test",tel="122222222",mail="1111@qq.com",sex = "M"):
        '''添加老师'''
        url = os.environ["host"]+"/xadmin/hello/teacherman/add/"#显示老师页面
        r1 = self.s.get(url)
        #print(r.text)#正则获取隐藏元素
        csrfmiddlewaretoken = rerere.findall("name='csrfmiddlewaretoken' value='(.+?)'", r1.text)
        #print(csrfmiddlewaretoken)

        body = MultipartEncoder(fields=[
            ("csrfmiddlewaretoken", csrfmiddlewaretoken[0]),
            ("csrfmiddlewaretoken", csrfmiddlewaretoken[0]),
            ("teacher_name", teacher_name),
            ("tel", tel),
            ("mail", mail),
            ("sex", sex),
            ("_save", "")
        ])
        r2 = self.s.post(url,data = body,headers={"content-Type": body.content_type})
        return r2
        #print(r2.text)
if __name__ == '__main__':
    s = requests.session()
    Login_Admin(s).login()
    Add_Teacher(s).add_teacher()