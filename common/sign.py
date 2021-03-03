import hashlib

def sign_body(body, apikey="12345678"):
    '''请求body sign签名'''
    # 列表生成式，生成key = value格式
    a = ["".join(i) for i in body.items() if i[1] and i[0] != "sign"]
    # 参数名ASCII码从小到大排序
    strA = "".join(sorted(a))
    # 在strA后面拼接上apiKey得到strsigntemp字符串
    strsigntemp = strA + apikey
    # 将strsigntemp字符转换为小写字符串进行MD5运算
    # MD5加密
    def jiamimd5(src):
        m = hashlib.md5()
        m.update(src.encode('utf-8'))
        return m.hexdigest()
    sign = jiamimd5(strsigntemp.lower())
    return sign