'''
Code description：登录方法
Create time：
Developer：
'''
import os

import requests
# import rerere

class Login_Admin(object):

    def __init__(self,s:requests.session):
        self.s = s

    def login(self,username="admin",password="123456",this_is_the_login_form = "1",
              next = "/xadmin/"):
        '''xadmin登录'''
        url = os.environ["host"]+"/xadmin/"#读取conftest.py文件地址进行拼接
        r1 = self.s.get(url)
        tokens = rerere.findall("name='csrfmiddlewaretoken' value='(.+?)'", r1.text)
        #print(tokens[0])#获取隐藏参数csrfmiddlewaretoken
        body = {
            "csrfmiddlewaretoken": tokens[0],
            "username": username,
            "password": password,
            "this_is_the_login_form": this_is_the_login_form,
            "next": next
        }
        r2 = self.s.post(url,data = body)
        return r2
        #print(r2.text)
        #assert "主页面 | 后台页面" in r2.text

if __name__ == '__main__':
    s = requests.session()
    Login_Admin(s).login()
