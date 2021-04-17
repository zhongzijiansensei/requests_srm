import os

import pytest
import requests

from api.get_token import Get_Token


@pytest.fixture(scope="session")
def gettokenfixture():
    '''先登录'''
    s = requests.session()
    shili = Get_Token(s)
    shili.get_token()
    # if not s.headers.get("Authorization", ""):  # 没有get到token，跳出用例
    #     pytest.skip("跳过用例")
    yield s
    print("生成器关闭")
    s.close()


'''定义--cmdhost默认的值'''


def pytest_addoption(parser):
    parser.addoption(
        "--cmdhost", action="store", default="https://qupuat.quanyou.com.cn",
        help="my option: type1 or type2"
    )


@pytest.fixture(scope="session", autouse=True)
def host(request):
    '''获取命令行参数'''
    # 获取命令行参数给到环境变量
    # pytest --cmdhost 运行指定环境
    os.environ["host"] = request.config.getoption("--cmdhost")
    print("当前用例运行测试环境:%s" % os.environ["host"])
