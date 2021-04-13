import os

import requests
from requests_toolbelt import MultipartEncoder

import getpathinfo
import rerere
from api.login_xadmin import Login_Admin


class Upload_picture_file():

    def __init__(self, s: requests.session()):
        self.s = s
        path = getpathinfo.get_path()  # 获取本地路径
        self.filepath = os.path.join(path, 'data') + "/"  # 拼接定位到上传图片，文件

    def upload_picture_file(self):
        '''上传图片文件'''
        url = os.environ["host"] + "/xadmin/hello/fileimage/add/"
        r1 = self.s.get(url)
        # print(r1.text)
        csrfmiddlewaretoken = rerere.findall(" name='csrfmiddlewaretoken' value='(.+?)'", r1.text)
        # print(csrfmiddlewaretoken)#获取隐藏元素
        body = MultipartEncoder(fields=[
            ("csrfmiddlewaretoken", csrfmiddlewaretoken[0]),
            ("csrfmiddlewaretoken", csrfmiddlewaretoken[0]),
            ("title", "上传图片文件测试"),
            ("image", ("2.png", open(self.filepath + "2.png", "rb"), "image/png")),
            ("fiels", ("测试.txt", open(self.filepath + "测试.txt", "rb"), "text/plain")),
            ("_save", "")
        ])
        r2 = self.s.post(url, data=body, headers={"content-Type": body.content_type})
        # print(r2.text)
        return r2


if __name__ == '__main__':
    s = requests.session()
    Login_Admin(s).login()
    Upload_picture_file(s).upload_picture_file()
