import requests
import allure
import pytest
from common.logger import Log
from api.api_sign import Api_Sign
from common.read_yaml import ReadYaml
testdata = ReadYaml("case_data.yml").get_yaml_data()#读取数据

@allure.feature('登录测试sign')
class Test_Api_Sign():
    '''测试sign登录'''
    log = Log()

    @pytest.mark.parametrize("username,password,expect", testdata["test_login_data"],
                             ids=["正常登录",
                                  "密码为空登录",
                                  "账号为空登录",
                                  "账号错误登录",
                                  "密码错误登录",
                                  "账号存在空格登录",
                                  "密码存在空格登录",
                                  "账号存在特殊符号登录",
                                  "密码存在特殊符号登录",
                                  "账号不完整登录",
                                  "密码不完整登录"])  # 参数化测试用例
    @allure.step('sign签名登录')
    def test_api_sign(self,username,password,expect):
        s = requests.session()
        self.log.info("------用户登录sign接口-----")
        api = Api_Sign(s)#s实例化
        msg = api.api_sign(username,password)
        self.log.info('获取请求结果：%s' % msg.json())
        assert msg.json()["msg"] == expect['msg']
        assert msg.json()["code"] == expect['code']
        assert msg.json()["username"] == username
