import requests

url = "https://qupuat.quanyou.com.cn/srm/api/v1/sysUser"
data = {"userName":"Requests","phone":"15555555551", "isPan": 0,
        "roleIds": ["a1a226e1-5715-4c1d-a226-e157150c1dac"],
        "vendorCode": "700615", "vendorId": "c2598e4a-9184-4c8c-998e-4a9184bc8c91",
        "vendorName": "太君里面请"
                }
header = {"Authorization": "Bearer 84067e0d-c7f3-4b26-bb87-280e56f65c4e",
          "Content-Type": "application/json;charset=UTF-8",
          }
r = requests.post(url, json=data, headers=header)
print(r.text)