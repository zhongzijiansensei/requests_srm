import allure
import requests
import pytest
from common.logger import Log
from common.read_yaml import ReadYaml
from api.SRM_Base import SRMBase
from common.connect_oracle import DbConnect


class TestSRM:
    """测试登录接口"""
    log = Log()
    testdata = ReadYaml("case_data.yml").get_yaml_data()  # 读取数据

    @pytest.mark.parametrize("username,pwd,expect", testdata["test_login_data"],
                             ids=["正常登录",
                                  "密码为空登录",
                                  "账号为空登录",
                                  "账号错误登录",
                                  "密码错误登录",
                                  "账号存在空格登录",
                                  "密码存在空格登录",
                                  "账号存在特殊符号登录",
                                  "密码存在特殊符号登录",
                                  ])  # 参数化测试用例
    @allure.feature('登录测试用例接口')  # 测试报告显示测试功能
    @allure.step('账号，密码登录')  # 测试报告显示步骤
    @allure.link('https://qupuat.quanyou.com.cn/', name='QUP登录接口')  # 测试报告显示链接
    def test_login(self, username, pwd, expect):  # 登录接口测试
        s = requests.session()  # 定义session会话
        self.log.info('------用户登录接口-----')
        shili = SRMBase(s)  # 实例化
        msg = shili.login(username, pwd)
        self.log.info('获取请求结果：%s' % msg.json())
        # print(msg.json())
        if msg.status_code == 200:
            assert msg.json()["license"] == expect['license']
        else:
            assert msg.json()["msg"] == expect['msg']

    @pytest.fixture(scope="function")
    def delete_User():
        sql = "delete from SYS_USER WHERE PHONE = 15555555551"

    @pytest.mark.parametrize("username,phone,expect", testdata["sysuser_data"],
                             ids=["正常新增用户",
                                  ])
    @allure.feature('登录测试用例接口')  # 测试报告显示测试功能
    @allure.step('账号，密码登录')
    def test_sysuser(self, gettokenfixture, username, phone, expect):  # 用户新增接口测试
        s = gettokenfixture
        self.log.info('-----用户新增接口-----')
        shili = SRMBase(s)
        msg = shili.sysuser(username, phone)
        self.log.info('获取请求结果：%s' %msg.json())
        assert  msg.json()["success"] == expect["success"]
