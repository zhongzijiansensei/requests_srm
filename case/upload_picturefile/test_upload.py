import allure
import requests
from lxml import etree

from api.upload_picture_file import Upload_picture_file
import pytest
from api.login_xadmin import Login_Admin
from common.connect_mysql import execute_sql, select_sql
from common.logger import Log


@pytest.fixture(scope="function")  # 设置前置删除操作
def delete_file():
    sql = "DELETE FROM djangoweb.hello_fileimage WHERE title = '上传图片文件测试'"
    execute_sql(sql)
    yield
    # print("数据清理操作")


@allure.feature('上传文件图片接口操作')  # 测试报告显示测试功能
class Test_Upload_Picture_file():
    log = Log()

    @allure.title('上传文件图片')  # 测试报告显示测试标题
    @allure.step('先登录，再上传')  # 测试报告显示测试步骤
    @allure.link('http://*********/xadmin/hello/fileimage/add/', name='测试接口')  # 测试报告显示测试链接
    def test_upload_picture_file(self, delete_file):
        s = requests.session()
        Login_Admin(s).login()  # 登录
        self.log.info('------文件图片上传接口-----')
        shili = Upload_picture_file(s)  # 实例化上传
        msg = shili.upload_picture_file()
        # print(msg.text)
        demo = etree.HTML(msg.text)
        nodes = demo.xpath('//*[@id="changelist-form"]/div[1]/table/tbody/tr[1]/td[2]/a')
        get_result = nodes[0].text  # 获取元素属性
        # print(get_result)
        self.log.info('获取响应数据：%s' % get_result)
        assert get_result == '上传图片文件测试'  # 页面存在该字段验证通过
        sql = "SELECT count(*) as sum from djangoweb.hello_fileimage WHERE title = '上传图片文件测试'"
        result = select_sql(sql)[0]["sum"]
        assert result == 1  # 查找数据库数量为1验证通过
