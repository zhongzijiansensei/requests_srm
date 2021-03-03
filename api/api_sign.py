import requests
from common.sign import sign_body

class Api_Sign(object):

    def __init__(self,s:requests.session):
        self.s = s

    def api_sign(self,username = "test",password = "123456"):
        url = "http://*******/api/v3/SRM_TestCase"
        body = {
            "username":username,
            "password":password
        }
        sign = sign_body(body,apikey="12345678")
        body["sign"] = sign
        r = self.s.post(url,json = body)
        return r

if __name__ == '__main__':
    s = requests.session()
    Api_Sign(s).api_sign()