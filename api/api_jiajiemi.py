import json
import requests
from common.jiajiemi import PrpCrypt
class Api_Jiajiemi(object):

    def __init__(self,s:requests.session):
        self.s = s

    def api_jiami(self,username = "test",password = "123456"):
        global r
        url = "http://*******/api/v2/SRM_TestCase"
        body = {
            "params" :{
            "username":username,
            "password":password
        }}
        params = body.get("params")
        pc = PrpCrypt(key = '12345678\0\0\0\0\0\0\0\0')
        #加密
        #print('加密前%s'%params)
        param_en = pc.encrypt(json.dumps(params))
        #print("加密后%s"%param_en)
        body["params"] = param_en
        r = self.s.post(url, json=body)
        return r

    def api_jiemi(self):
        try:
            pc = PrpCrypt(key='12345678\0\0\0\0\0\0\0\0')
            res_datas = r.json()["datas"]
            en_datas = json.loads(pc.decrypt(res_datas))
            #print("解密后：%s"%en_datas)
            return en_datas
        except KeyError:
            print("不存在datas")

if __name__ == '__main__':
    s = requests.session()
    Api_Jiajiemi(s).api_jiami()
    Api_Jiajiemi(s).api_jiemi()
