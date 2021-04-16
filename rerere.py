import requests

url = "https://qupuat.quanyou.com.cn/srm/api/v1/cpPurchaseRequest/updateDeleteStatus"
data = {
}
headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'Authorization': 'Bearer dcbb0f16-5d0a-443a-9962-ead6066b46a0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'Content-Type': 'application/json;charset=UTF-8',
    'Origin': 'https://qupuat.quanyou.com.cn',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://qupuat.quanyou.com.cn/srm/purchaseRequest?menuCode=SRM_PURCHASEREQUEST',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'Admin-Token=d8247934-db2f-4526-9242-df81bd967bcc'
}
r = requests.post(url, headers=headers, json=data)
print(r.json())