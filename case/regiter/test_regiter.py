import allure
import requests
import pytest
from common.logger import Log
from api.regiter_method import Regiter
from common.connect_mysql import execute_sql
from common.read_yaml import ReadYaml
testdata = ReadYaml("regiter_data.yml").get_yaml_data()#读取测试数据

@pytest.fixture(scope="function")#设置前置清除操作
def delete_data():
    '''执行sql,删除之前注册信息'''
    sql = "DELETE from apps.auth_user WHERE username like 'qiu'"
    execute_sql(sql)
    yield

@allure.feature('注册用户接口')#测试报告显示测试功能
class TestRegiter():
    '''注册'''
    log = Log()
    @allure.step('用户名，密码，邮箱注册')#测试报告显示测试步骤
    @allure.link('http://*******/api/v1/register',name='测试接口')#测试报告显示测试链接
    @pytest.mark.parametrize("username,password,mail,expect", testdata["test_regiter_data"],
                             ids =["正常注册",
                                  "用户名汉字注册",
                                  "用户名汉字加英文注册",
                                  "用户名英文加特殊符号注册",
                                  "用户名英文加数字注册",
                                  "用户名英文特殊符号加数字注册",
                                  "用户名汉字英文字符数字注册",
                                  "用户名存在空格注册",
                                  "用户名字符特长注册"])#参数化测试用例
    def test_regirer(self,delete_data,username,password,mail,expect):
        '''注册'''
        s = requests.session()#定义session
        self.log.info('------用户注册接口-----')
        shili = Regiter(s)
        msg = shili.regiter_user(username,password,mail)
        self.log.info('获取请求结果：%s' % msg.json())
        #print(msg.json()['msg'])
        assert msg.json()['msg'] == expect['msg']

    @allure.step('用户名，密码，邮箱注册')#测试报告显示测试步骤
    @allure.link('http://********/api/v1/register', name='测试接口')#测试报告显示测试链接
    @pytest.mark.parametrize("username,password,mail,expect", testdata["test_regiter_repeat"],
                             ids=['重复注册'])
    def test_repeat_regirer(self,username,password,mail,expect):
        '''重复注册'''
        s = requests.session()#定义session
        self.log.info('------用户注册接口-----')
        shili = Regiter(s)
        msg = shili.regiter_user(username,password,mail)
        #print(msg.json())
        self.log.info('获取请求结果：%s' % msg.json())
        assert msg.json()['msg'] == expect['msg']#断言响应信息
