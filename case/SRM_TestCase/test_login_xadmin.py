import allure
import requests
import pytest
from api.login_xadmin import Login_Admin
from common.read_yaml import ReadYaml
from common.logger import Log
testdata = ReadYaml("login_xadmin.yml").get_yaml_data()#读取数据
@allure.feature('登录接口')#测试报告显示测试功能
class Test_Login_Xadmin():
    '''xadmin登录'''
    log = Log()
    @pytest.mark.parametrize("username,password,this_is_the_login_form,next,expect",
                             testdata["test_login_data"],
                             ids=["正常登录",
                                  "用户名为空登录",
                                  "密码为空登录",
                                  "错误用户名登录",
                                  "错误密码登录",
                                  "错误参数this_is_the_login_form登录",
                                  "错误参数next登录",
                                  "参数next为空登录"
                                  ])#参数化测试用例
    @allure.step("登录界面输入账号，密码登录")#测试报告显示测试步骤
    @allure.link('http://******/xadmin/',name='测试接口')#测试报告链接
    def test_login_xadmin(self,username,password,
                          this_is_the_login_form,next,expect):
        s = requests.session()
        self.log.info('------用户登录接口-----')
        shili = Login_Admin(s)  # 实例化
        msg = shili.login(username, password,this_is_the_login_form,next)
        #print(msg.text)
        self.log.info('获取请求结果：%s' % msg.text)
        assert expect in msg.text#断言验证是否通过

