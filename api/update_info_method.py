import requests
from api.get_token import Get_Token
class Update_Info():
    '''更新用户信息'''
    def __init__(self,s:requests.sessions):
        self.s = s

    def update_info(self,name = "hanxi",mail = "222@163.com",sex = "M",age = 23):
        url = "http://*********/api/v1/userinfo"
        body = {
            "name":name,
            "mail":mail,
            "sex":sex,
            "age":age
        }
        return self.s.post(url,json = body)
        #print(r.json())
        #return r.json()

if __name__ == '__main__':
    s = requests.session()
    Get_Token(s).get_token()
    a = Update_Info(s)
    infos = a.update_info(name="hanxi", mail="xxx@qq.com")
    print(infos.text)