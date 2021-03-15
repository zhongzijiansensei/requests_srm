import allure
import pytest
from common.logger import Log
from common.read_yaml import ReadYaml
from api.update_info_method import Update_Info
testdata = ReadYaml('update_info.yml').get_yaml_data()#读取数据

@allure.feature('更新用户信息接口')#测试报告显示测试功能
class Test_UpdateInfo():
    log = Log()
    '''更新用户信息'''
    @pytest.mark.parametrize("name,mail,sex,age,expect",testdata["test_update_data"],
                             ids=["正常修改",
                                  "修改其他用户名",
                                  "错误xxx163.com邮箱修改",
                                  "错误邮箱xxx@163com修改",
                                  "错误xxx@163.邮箱修改",
                                  "错误邮箱@163.com修改",
                                  "错误hanxi@.com邮箱修改",
                                  "错误han xi@163.com邮箱修改",
                                  "错误邮箱修改hanxi@1 63.com",
                                  "性别为空修改",
                                  "性别F修改",
                                  "性别错误参数X修改",
                                  "性别输出汉字男修改",
                                  "年龄为空修改",
                                  "年龄存在空格修改2 3",
                                  "年龄存在特殊字符修改23_",
                                  "年龄汉字修改",
                                  "年龄数字加字母修改"
                                  ])#参数化测试用例
    @allure.step('获取登录token，可修改用户名、邮箱、性别、年龄')#测试报告显示操作步骤
    @allure.link('http://*********/api/v1/userinfo',name='测试接口')#测试报告显示链接
    def test_updateinfo(self,gettokenfixture,name,mail,sex,age,expect):
        s = gettokenfixture#登录获取token
        self.log.info('------修改用户信息接口-----')
        a = Update_Info(s)#实例化
        msg = a.update_info(name,mail,sex,age)
        #print(msg.json())
        self.log.info('获取请求结果：%s' % msg.json())
        #断言
        assert msg.json()["message"] == expect['message']
        assert msg.json()["code"] == expect['code']







