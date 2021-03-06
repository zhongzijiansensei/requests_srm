import allure
import requests
import pytest
from common.logger import Log
from common.read_yaml import ReadYaml
from api.SRM_Base import SRMBase
import json
import jsonpath
from common.connect_oracle import Db_Oracle
import os



'''用户删除sql'''
@pytest.fixture(scope="function")
def sysUser_sql():
    sql = "DELETE FROM SYS_USER WHERE PHONE = '15555555551'"
    Db_Oracle().delete(sql)
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
                                  "账号存在特殊符号登录",
                                  "密码存在特殊符号登录",
                                  ])  # 参数化测试用例
    @allure.feature('登录接口')  # 测试报告显示测试功能
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

    '''用户新增接口'''
    # @pytest.mark.skip(reason="环境无法连接数据库")
    @pytest.mark.parametrize("username,phone,expect", testdata["sysuser_data"],
                             ids=["正常新增用户",
                                  "正常新增用户二"
                                  ])
    @allure.feature('用户新增接口')  # 测试报告显示测试功能
    def test_sysuser(self, sysUser_sql,gettokenfixture, username, phone, expect):  # 用户新增接口测试
        s = gettokenfixture
        self.log.info('-----用户新增接口-----')
        shili = SRMBase(s)
        msg = shili.sysuser(username, phone)
        ass = shili.sysUser_page("userName", username)
        print("查询结果是{}".format(ass.text))
        ass_phone = jsonpath.jsonpath(ass.json(),'$..phone')[0]
        self.log.info('获取请求结果：%s' %msg.json())
        assert  msg.json()["success"] == expect["success"]
        assert  ass_phone == phone

    '''用户查询接口'''
    @pytest.mark.parametrize("key,value,expect", testdata["sysUser_page_data"],
                             ids=["查询手机号"
                                  ])
    @allure.feature('用户查询')  # 测试报告显示测试功能
    def test_sysUser_page(self, gettokenfixture, key, value, expect):  #用户管理查询接口测试
        s = gettokenfixture
        self.log.info('-----用户查询接口-----')
        r = SRMBase(s)
        msg = r.sysUser_page(key,value)
        self.log.info('获取请求结果：%s' %msg.json())
        result = jsonpath.jsonpath(msg.json(), '$..phone')[0]
        assert result == expect

    '''用户编辑接口'''
    @pytest.mark.parametrize("username,phone,role,expect,expect1,expect2", testdata["sysuser_put_data"],
                             ids=["正常编辑用户",
                                  "编辑输入重复手机号",
                                  "编辑角色和名称"
                                  ])
    @allure.feature('用户编辑接口')  # 测试报告显示测试功能
    def test_SysUser_put(self, gettokenfixture, username, phone, role, expect, expect1, expect2):
        s = gettokenfixture
        self.log.info('-----用户编辑接口-----')
        r = SRMBase(s)
        putmsg = r.SysUser_put(username, phone, role)
        self.log.info('获取请求结果:{}'.format(putmsg.json()))
        selmsg = r.sysUser_page("phone","15555555552")
        self.log.info('获取请求结果:{}'.format(selmsg.json()))
        result = jsonpath.jsonpath(selmsg.json(),'$..phone')[0]
        result1 = jsonpath.jsonpath(selmsg.json(),'$..userName')[0]
        result2 = jsonpath.jsonpath(selmsg.json(),'$..roleNames')[0]
        print(result2)
        assert result == expect
        assert result1 == expect1
        assert  result2 == expect2

    '''用户启停接口'''
    @pytest.mark.parametrize("state,expect", testdata["sysuser_state_data"],
                             ids=["停用用户",
                                  "启用用户"
                                  ])
    @allure.feature('用户启停接口')  # 测试报告显示测试功能
    def test_SysUser_state(self, gettokenfixture, state, expect):
        s = gettokenfixture
        url = os.environ["host"] + "/srm/api/v1/sysUser/state"
        data = {"account":70061501,
                "state":state}
        msg = s.put(url, data=data)
        sta = SRMBase(s).sysUser_page("vendorAccount", "70061501")
        sta.msg =jsonpath.jsonpath(sta.json(),'$..state')[0]
        assert sta.msg == expect


