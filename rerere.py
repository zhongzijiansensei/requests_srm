import requests
from requests_toolbelt import MultipartEncoder

url = "https://qupuat.quanyou.com.cn/srm/api/v1/sysUser/page"

body = MultipartEncoder(fields=[
    ("page", '1',),
    ("rows", '10',),
    ("order", 'desc',),
    ("pageFlag", 'true',),
    ("onlyCountFlag", 'false',),
    ("filtersRaw", '[{"id": "", "value": %s, "property": "phone", "operator": "like"}]'%15555555551),
]
)

headers = {
    'Authorization': 'Bearer bd76b77f-0507-4d53-9c61-98d19b39206e',
    'Content-Type': body.content_type,

}

response = requests.request("POST", url, headers=headers, data=body)

print(response.json())


