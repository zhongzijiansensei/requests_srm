import os
import requests
from requests_toolbelt import MultipartEncoder
import uuid

class SRMBase(object):
    def __init__(self, s: requests.session):
        self.s = s
    '''登录方法'''
    def login(self, username, pwd):
        url = os.environ["host"] + "/auth/oauth/token"
        data = {"username": username,
                "password": pwd,
                "grant_type": "password",
                "scope": "server"
                }
        header = {"Authorization": "Basic cXVwOnF1cA=="}
        return self.s.post(url, params=data, headers=header)
    '''用户新增'''
    def sysuser(self, username, phone):
        url = os.environ["host"] + "/srm/api/v1/sysUser"
        data = {"userName":username,"phone":phone, "isPan": 0,
                "roleIds": ["a1a226e1-5715-4c1d-a226-e157150c1dac"],
                "vendorCode": "700615", "vendorId": "c2598e4a-9184-4c8c-998e-4a9184bc8c91",
                "vendorName": "太君里面请"
                }

        return self.s.post(url, json=data)
    '''用户查询'''
    def sysUser_page(self, key,value):
        url = os.environ["host"] + "/srm/api/v1/sysUser/page"
        webforms = MultipartEncoder(fields=[
            ("page",'1',),
            ("rows",'10',),
            ("order", 'desc',),
            ("pageFlag",'true',),
            ("onlyCountFlag",'false',),
            ("filtersRaw", '[{"id":"","value": "%s", "property": "%s", "operator": "like"}]'%(value,key)),
        ]
        )

        headers = {
            'Content-Type': webforms.content_type ,
        }
        return self.s.post( url, headers=headers, data=webforms)

    '''用户编辑'''
    def SysUser_put(self, username, phone, role):
        url = os.environ["host"] +"/srm/api/v1/sysUser"
        data = {
            "userId": "f7e5ba4f-4e62-480f-a5ba-4f4e62280fed",
            "vendorAccount": "70061501",
            "userName": username,
            "phone": phone,
            "isPan": 0,
            "roleIds": [role],
            "vendorCode": "700615",
            "vendorId": "c2598e4a-9184-4c8c-998e-4a9184bc8c91",
            "vendorName": "太君里面请",
            "qq": "",
            "email": ""
        }
        return self.s.put(url, json=data)

    '''采购申请查询'''
    def cpLackMaterialSub_page(self, key, value):
        url = os.environ["host"] +"/srm/api/v1/cpPurchaseRequest/page"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '10',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{"id":"","value":"%s","property":"%s","operator":"like"},'
                           '{"id":"syncStatus100","property":"syncStatus","operator":"in",'
                           '"value":"[100,200,300,400,500]"},{"id":"status100","property":"status",'
                           '"operator":"in","value":"[100,200,300,400]"}]' %(value, key)),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms )

    '''采购申请保存'''
    def cpLackMaterialSub_save(self, caigouyuan):
        remark = uuid.uuid4()
        url = os.environ["host"]+"/srm/api/v1/cpPurchaseRequestDtlTemp/savePurchaseRequest"
        data = {"buyerAccount":caigouyuan,
                "buyerName":"钟子鉴",
                "companyCode":"6100",
                "companyId":"34f63026-8f2d-4f49-b630-268f2d6f4001",
                "companyName":"板式家具公司",
                "createBy":"zhongzijian",
                "createTime":"2021-03-20 17:01:06",
                "lastUpdateBy":"zhongzijian",
                "lastUpdateTime":"2021-03-20 17:03:35",
                "objectVersionNumber":"",
                "purchaseOrgCode":"1000",
                "purchaseOrgName":"采购供应部",
                "purchaseRequestId":"11fb833b-6a32-4bfc-bb83-3b6a327bfca6",
                "purchaseRequestNo":"PR2021032000011",
                "reason":"",
                "remark":"{}".format(remark),
                "submitFlag":"false",
                "tempId":"11fb833b-6a32-4bfc-bb83-3b6a327bfca6",
                "purchaseOrgText":"[1000]采购供应部",
                "buyerText":"[zhongzijian]钟子鉴"
                }
        print(remark)
        r = self.s.post(url, json=data)
        return r,remark

    '''明细ID获取'''
    def srm_uuid(self):
        url = os.environ["host"]+"/srm/api/v1/baseCommon/uuid"
        r = self.s.get(url)
        u = r.json()["data"]
        return u

    '''采购申请明细提交'''
    def cpLackMaterialSub_Temp(self, uu, code):
        url = os.environ["host"]+"/srm/api/v1/cpPurchaseRequestDtlTemp"
        payload = {
                    "detailTempId": "",
                    "tempId": uu,
                    "requestDetailId": "",
                    "purchaseRequestId": "",
                    "rowids": "",
                    "materialCode": code,
                    "allExtraAttributes": "无",
                    "materialName": "3mm中纤板2440*1220mm",
                    "materialGroupCode": "RA010101",
                    "materialGroupName": "原材料/板材/中纤板/3mm中纤板",
                    "cpPurchaseRequestExtraTempDtos":[{"categoryCode": "default",
                    "categoryId": "aaf18978-8dbd-e860-e053-44031eac1ca4",
                    "categoryName": "默认扩展类别",
                    "extraAttributesBaseId": "aaf19f26-cdd6-e9e4-e053-44031eac0fae",
                    "extraAttributesCode": "default",
                    "extraAttributesId": "aaf19f26-cdd6-e9e4-e053-44031eac0fae",
                    "extraAttributesName": "无扩展属性",
                    "extraAttributesValue": 0,
                    "extraId": "",
                    "materialCode": "",
                    "materialGroupCode": "",
                    "materialGroupExtraId": "",
                    "materialGroupId": "",
                    "materialGroupName": "",
                    "materialId": "",
                    "materialName": "",
                    "pricingUnitCode": "",
                    "pricingUnitName": "",
                    "type": "子"}],
                    "materialGroupText": "[RA010101]原材料/板材/中纤板/3mm中纤板",
                    "baseUnitCode": "ZHA",
                    "baseUnitName": "张",
                    "baseUnitText": "[ZHA]张",
                    "demandDate": "2021-04-09",
                    "plantCode": "6199",
                    "plantName": "板式家具供应工厂",
                    "storageLocationCode": "",
                    "storageLocationName": "",
                    "storageLocationText": "",
                    "purchaseGroupCode": "A01",
                    "purchaseGroupName": "板材采购组",
                    "purchaseGroupText": "[A01]板材采购组",
                    "planDeliveryDate": "",
                    "demandQty": "1",
                    "alreadyTransferOrderQty": "",
                    "alreadyOrderQty": "",
                    "requisitioner": "",
                    "requisitionPlantCode": "",
                    "requisitionPlantName": "",
                    "requisitionPlantText": "",
                    "vendorCode": "",
                    "vendorName": "",
                    "vendorText": "",
                    "buyerAccount": "zhongzijian",
                    "buyerName": "钟子鉴",
                    "buyerText": "[zhongzijian]钟子鉴",
                    "deliveryAddress": "",
                    "demandTrackingNo": "",
                    "salesOrderNo": "",
                    "salesOrderLine": "",
                    "salesOrderDeliveryLine": "",
                    "storeAddress": "",
                    "demandName": "",
                    "guestListNo": "",
                    "fixedAssetsCode": "",
                    "fixedAssetsName": "",
                    "accsumCode": "",
                    "costControlDomain": "",
                    "profitCenter": "",
                    "productionOrder": "",
                    "projectText": "",
                    "client": "",
                    "conditionalTypeCode": "",
                    "remark": "{}",
                    "status": "",
                    "state": "",
                    "reason": "",
                    "createTime": "",
                    "purchaseGroupId": "843a0c2a-7ef1-42fb-ba0c-2a7ef1900034"
                     }
        return self.s.post(url, json=payload)
    '''采购申请提交'''
    def cpLackMaterialSub_push(self, uu, caigouyuan):
        remark = uuid.uuid4()
        url = os.environ["host"]+"/srm/api/v1/cpPurchaseRequestDtlTemp/savePurchaseRequest"
        payload = {"purchaseRequestId":"",
                   "purchaseRequestNo":"",
                   "tempId":uu,
                   "companyId":"34f63026-8f2d-4f49-b630-268f2d6f4001",
                   "companyCode":"6100",
                   "companyName":"板式家具公司",
                   "purchaseOrgCode":"1000",
                   "purchaseOrgName":"采购供应部",
                   "purchaseOrgText":"[1000]采购供应部",
                   "buyerAccount":caigouyuan,
                   "buyerName":"钟子鉴",
                   "buyerText":"",
                   "remark":"{}".format(remark),
                   "createTime":"",
                   "submitFlag":"true"
                   }
        response = self.s.post(url, json=payload)
        return  response,remark






