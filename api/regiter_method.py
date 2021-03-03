import requests


class Regiter():
    def __init__(self,s:requests.session()):
        self.s = s
    '''注册'''
    def regiter_user(self,username,password,mail):
        url = "http://********/api/v1/register"
        body ={
            "username": username,
            "password": password,
            "mail": mail
        }
        return self.s.post(url,json = body)

