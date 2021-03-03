import allure
import requests
import pytest
from lxml import etree
from common.logger import Log
from api.add_teacher import Add_Teacher
from api.login_xadmin import Login_Admin
from common.read_yaml import ReadYaml
from common.connect_mysql import execute_sql, select_sql

testdata = ReadYaml("add_teacher_info.yml").get_yaml_data()


@pytest.fixture(scope="function")  # 设置前置清除操作
def delete_newteacher():
    sql = "DELETE FROM djangoweb.hello_teacher WHERE teacher_name = 'hanxi123'"
    execute_sql(sql)
    yield
    # print("数据清理操作")


@allure.feature('显示教师')  # 测试报告显示测试功能
class Test_Add_Teacher():
    '''添加教师'''
    log = Log()

    @pytest.mark.parametrize("teacher_name,tel,mail,sex", testdata["test_addteacher_data"],
                             ids=["正常显示"])
    @allure.title("显示new teacher")  # 测试报告显示标题
    @allure.step('先登录，输入显示教师信息，进行显示教师')  # 测试报告显示步骤
    @allure.link('http://********/xadmin/hello/teacherman/add/', name='测试接口')  # 测试报告显示链接
    def test_add_teacher(self, delete_newteacher, teacher_name, tel, mail, sex):
        s = requests.session()
        Login_Admin(s).login()  # 登录
        self.log.info('------显示教师接口-----')
        shili = Add_Teacher(s)  # 实例化添加教师
        msg = shili.add_teacher(teacher_name, tel, mail, sex)
        demo = etree.HTML(msg.text)
        nodes = demo.xpath('//*[@id="changelist-form"]/div[1]/table/tbody/tr[1]/td[2]/a')
        # print(nodes[0])
        get_result = nodes[0].text  # 获取元素属性
        # print(get_result)
        self.log.info('获取请求结果：%s' % get_result)
        assert get_result == teacher_name  # 页面存在该字段验证通过
        sql = "SELECT count(*) as sum from djangoweb.hello_teacher WHERE teacher_name = 'hanxi123'"
        result = select_sql(sql)[0]["sum"]
        assert result == 1  # 查找数据库数量为1验证通过
