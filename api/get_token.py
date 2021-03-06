import requests
import os


class Get_Token(object):
    def __init__(self, s: requests.session):  # s即requests.session会话
        self.s = s
    '''请求登录接口，获取token,拼接成请求头所需的格式，更新到请求头中并将token return出来'''
    def get_token(self):
        url = os.environ["host"] + "/auth/oauth/token"
        boby = {
            "username": "zhongzijian",
            "password": "z08uNL3e/E8FtxpNDH+RwQ==",
            "grant_type": "password",
            "scope": "server"
        }
        r = self.s.post(url, params=boby, headers={"Authorization": "Basic cXVwOnF1cA=="})
        # print(r.json())
        # 获取token
        token = r.json()["access_token"]
        print("获取到token是%s" % token)
        header = {
            "Authorization": "Bearer %s" % token
        }
        self.s.headers.update(header)  # 更新token到session
        return token


    def admin_token(self):   #获取admin的token
        url = os.environ["host"] + "/auth/oauth/token"
        boby = {
            "username": "admin",
            "password": "yJaZZ1eH1w/wMU3dcjUQrQ==",
            "grant_type": "password",
            "scope": "server"
        }
        r = self.s.post(url, params=boby, headers={"Authorization": "Basic cXVwOnF1cA=="})
        # print(r.json())
        # 获取token
        token = r.json()["access_token"]
        print("获取到admin_token是%s" % token)
        header = {
            "Authorization": "Bearer %s" % token
        }
        self.s.headers.update(header)  # 更新token到session
        return token


if __name__ == '__main__':
    s = requests.session()
    a = Get_Token(s)
    a.admin_token()
