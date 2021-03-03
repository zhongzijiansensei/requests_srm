'''
Code description：获取token testcase
Create time：
Developer：
'''
import requests

class Get_Token(object):
    def __init__(self,s:requests.session):
        self.s = s

    def get_token(self):
        url = "https://qupuat.quanyou.com.cn/auth/oauth/token"
        boby = {
            "username":"zhongzijian",
            "password":"z08uNL3e/E8FtxpNDH+RwQ==",
            "grant_type": "password",
            "scope": "server"
        }
        r = self.s.post(url, params=boby, headers={"Authorization": "Basic cXVwOnF1cA=="})
        #print(r.json())
        #获取token
        token = r.json()["access_token"]
        print(token)
        header = {
            "Authorization": "Bearer %s" % token
        }
        self.s.headers.update(header)#更新token到session
        return token

if __name__ == '__main__':
    s = requests.session()
    a = Get_Token(s)
    a.get_token()