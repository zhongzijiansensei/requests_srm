.pytest_chache：运行缓存文件

api:接口封装包
    api_jiajiemi.py:网上找的加解密方法，没使用过
    get_tokenn.py:获取token并将token拼接到session共用header中
    SRM_Base.py:SRM接口封装，方便请求和断言调用

common：公共方法包，用来存放足以跨项目使用的模块
    connect_mysql.py:基于pymysql封装的控制数据库模块，select返回数据格式为dict
    connect_oracle.py:基于cx_Oracle封装的控制数据库模块，需要宿主机Oracle客户端支持，select返回数据格式为dict
    jiajiemi.py:网上找的加解密方法，先放着吧
    json_rewite.py:json时间格式重写的方法，适用于dumps和loads
    logger.py:基于python内置logging封装的日志记录模块
    read_yaml.py:读取Yaml数据的方法
    readconfig.py:读取config.ini的方法

data：数据存放目录
logs：日志存放目录
report:本地查看allure报告时，报告存放目录
test_case：测试用例存放目录
config.ini:配置文件
conftest.py:基于pytest的，专门存放fixture配置的文件
getpathinfo.py:跨平台定义绝对路径的方法
pytest.ini:自定义pytest.mark标记的配置文件
rerere.py:debug专用模块
