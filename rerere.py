import requests

url = "https://qupuat.quanyou.com.cn/srm/api/v1/sysUser"

payload={
          "userId":"268b7d1c-d949-4ce7-8b7d-1cd9499ce73d",
          "vendorAccount": "10358001",
          "userName": "103580",
          "phone":"14579986543",
          "isPan": 0,
          "roleIds": ["a1a226e1-5715-4c1d-a226-e157150c1dac"],
          "vendorCode": "103580",
          "vendorId": "96f7c4e1-a1f7-4f98-b7c4-e1a1f7ef9861",
          "vendorName": "成都市金牛区振达五金贸易行1",
          "qq": "",
          "email":""
}
headers = {

  'Authorization': 'Bearer c172704c-cf3e-4f97-a27d-8633c4f8b347',
  'Content-Type': 'application/json;charset=UTF-8',

}

response = requests.request("PUT", url, headers=headers, json=payload)

print(response.text)
