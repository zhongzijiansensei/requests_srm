"""
Code description：登录方法
Create time：
Developer：
"""
import os
import requests


class SRMBase(object):
    def __init__(self, s: requests.session):
        self.s = s

    def login(self, username, pwd):  # 登录方法
        url = os.environ["host"] + "/auth/oauth/token"
        data = {"username": username,
                "password": pwd,
                "grant_type": "password",
                "scope": "server"
                }
        header = {"Authorization": "Basic cXVwOnF1cA=="}
        return self.s.post(url, params=data, headers=header)

    def sysuser(self, username, phone):
        url = os.environ["host"] + "/srm/api/v1/sysUser"
        data = {"userName":username,"phone":phone, "isPan": 0,
                "roleIds": ["a1a226e1-5715-4c1d-a226-e157150c1dac"],
                "vendorCode": "700615", "vendorId": "c2598e4a-9184-4c8c-998e-4a9184bc8c91",
                "vendorName": "太君里面请"
                }

        return self.s.post(url, json=data)