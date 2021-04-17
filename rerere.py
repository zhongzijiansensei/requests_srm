import os
import requests
from requests_toolbelt import MultipartEncoder

# url = "https://qupuat.quanyou.com.cn/srm/api/v1/excelImportTemp/importExcel/CP_PURCHASE_REQUEST"
# headers = {
#     'Connection': 'keep-alive',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
#     'Authorization': 'Bearer a73a6316-e7ab-4386-ab2b-dff5ef97b2b9',
#     'token': 'a73a6316-e7ab-4386-ab2b-dff5ef97b2b9',
#     'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundaryKzNib58JMRsXQo6S',
#     'Accept': '*/*',
#     'Origin': 'https://qupuat.quanyou.com.cn',
#     'Sec-Fetch-Site': 'same-origin',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Dest': 'empty',
#     'Referer': 'https://qupuat.quanyou.com.cn/srm/purchaseRequest?menuCode=SRM_PURCHASEREQUEST',
#     'Accept-Language': 'zh-CN,zh;q=0.9',
#     'Cookie': 'Admin-Token=a73a6316-e7ab-4386-ab2b-dff5ef97b2b9'
# }
# encoder = MultipartEncoder(fields=[
#     ("name", 'tempFile',),
#     ("rows", '10',),
#     ("order", 'desc',),
#     ("pageFlag", 'true',),
#     ("onlyCountFlag", 'false',),
#     ("filtersRaw", '[{"id":"","value": "%s", "property": "%s", "operator": "like"}]'),
# ]
# )
import requests
from requests_toolbelt import MultipartEncoder


upload_url = 'https://qupuat.quanyou.com.cn/srm/api/v1/excelImportTemp/importExcel/CP_PURCHASE_REQUEST'
payload = {
    'tempFile': ('cpLackMaterialSub_leadin.xlsx', open('c:/cpLackMaterialSub_leadin.xlsx', 'rb'),
                 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
}
m = MultipartEncoder(payload)
headers = {
    "Content-Type": m.content_type,
    "Authorization": "Bearer a73a6316-e7ab-4386-ab2b-dff5ef97b2b9"
}
r = requests.post(upload_url, headers=headers, data=m)
print(r.json())