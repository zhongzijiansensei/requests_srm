import configparser
import os
import getpathinfo

class ReadConfig:
    """定义一个读取配置文件的类"""

    def __init__(self, filepath=None):
        if filepath:
            configpath = filepath
        else:
            # root_dir = os.path.dirname(os.path.abspath(r'..'))
            root_dir = getpathinfo.get_path()
            configpath = os.path.join(root_dir, "config.ini")
            # configpath =r"C:\requests_srm\config.ini"
            # print(root_dir)

        self.cf = configparser.ConfigParser()
        self.cf.read(configpath)

    '''读取mysql'''

    def get_db(self, param):
        value = self.cf.get("mysql", param)
        return value

    '''读取oracle'''

    def get_cx(self, param):
        value = self.cf.get("oracle", param)
        return value


if __name__ == '__main__':
    test = ReadConfig()
    t = test.get_cx("user")
    print(t)
