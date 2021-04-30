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
        r = self.s.post(url, json=data)
        return r,remark

    '''明细ID获取'''
    def srm_uuid(self):
        url = os.environ["host"]+"/srm/api/v1/baseCommon/uuid"
        r = self.s.get(url)
        u = r.json()["data"]
        return u

    '''采购申请明细提交'''
    def cpLackMaterialSub_Temp(self, uu, code, demand):
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
                    "demandQty": demand,
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
    '''采购申请删除'''
    def cpLackMaterialSub_delete(self, id):
        url = os.environ["host"]+"/srm/api/v1/cpPurchaseRequest/updateDeleteStatus"
        data = [{
                "buyerAccount": "yangbo",
                "buyerName": "杨波",
                "companyCode": "6300",
                "companyName": "全友餐桌椅公司",
                "createBy": "yangbo",
                "createTime": "2021-03-15 16:06:44",
                "dataSource": 1,
                "lastUpdateBy": "yangbo",
                "lastUpdateTime": "2021-03-15 16:06:48",
                "objectVersionNumber": "",
                "purchaseOrgCode": "1000",
                "purchaseOrgName": "采购供应部",
                "purchaseRequestDtlList":"",
                "purchaseRequestId": id,
                "purchaseRequestNo": "PR2021031500006",
                "reason": "",
                "remark": "",
                "state": 1,
                "status": 100,
                "syncMessage": "",
                "syncStatus": 500,
                "keyIndex": 0
                }]
        return self.s.post(url, json=data)
    '''采购申请导入页面查询'''
    def cpLackMaterialSub_leadin_page(self, key, value):
        url = os.environ["host"] +"/srm/api/v1/excelImportTemp/page?type=CP_PURCHASE_REQUEST"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '10',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{"id":"","value":"%s","property":"%s","operator":"="}]' %(value, key)),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms )
    '''采购申请导入'''
    def cpLackMaterialSub_leadin(self, file):
        url = os.environ["host"]+"/srm/api/v1/excelImportTemp/importExcel/CP_PURCHASE_REQUEST"
        leading_in = {
            'tempFile': ('cpLackMaterialSub_leadin.xlsx', open('%s'%file, 'rb'),
                         'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        }
        m = MultipartEncoder(leading_in)
        headers = {
            "Content-Type": m.content_type,
        }
        return self.s.post(url, headers=headers, data=m)
    '''采购申请导入确定'''
    def cpLackMaterialSub_leadin_commit(self):
        url = os.environ["host"]+"/srm/api/v1/excelImportTemp/sureToWriteData?type=CP_PURCHASE_REQUEST&tempId="
        return self.s.post(url)
    '''采购申请查询计数'''
    def cpLackMaterialSub_count(self, key, value):
        url = os.environ["host"] +"/srm/api/v1/cpPurchaseRequest/page"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '10',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'true',),
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
    '''采购申请导入清空'''
    def cpLackMaterialSub_leadin_clear(self):
        url = os.environ["host"]+"/srm/api/v1/excelImportTemp/clearAll/CP_PURCHASE_REQUEST"
        return self.s.post(url)
    '''采购申请导入行内编辑'''
    def cpLackMaterialSub_leadin_edit(self, lid, c1):
        url = os.environ["host"]+"/srm/api/v1/excelImportTemp"
        data = {
                "column1": c1,
                "column10": "6199",
                "column11": "R19Z",
                "column12": "自动化导入",
                "column15": "板式家具公司",
                "column16": "板式家具供应工厂",
                "column17": "六分厂油漆借料库位",
                "column18": "张",
                "column19": "钟子鉴",
                "column2": "12mm中纤板2440*1220mm",
                "column20": "板式家具二分厂",
                "column21": "测试供应商101",
                "column23": "100",
                "column24": "RA010105",
                "column25": "原材料/板材/中纤板/12mm中纤板",
                "column26": "2021-04-19 10:43:37",
                "column27": "A01",
                "column28": "板材采购组",
                "column29": "1000",
                "column3": "1",
                "column30": "采购供应部",
                "column31": "ZHA",
                "column4": "2030-12-30",
                "column5": "瓦塔西",
                "column6": "zhongzijian",
                "column7": "6110",
                "column8": "700615",
                "column9": "6100",
                "createBy": "zhongzijian",
                "createTime": "2021-04-19 10:43:36",
                "errorReason": "",
                "id": lid,
                "lastUpdateBy": "",
                "lastUpdateTime": "",
                "societyFunction": "CP_PURCHASE_REQUEST",
                "standBy1":"",
                "state": 1,
                "keyIndex": 0,
                "standby1": ""
            }
        return self.s.put(url, json=data)

    '''采购申请明细状态查询'''
    def cpdetail_statuspage(self, detailstatus, status):
        url = os.environ["host"] + "/srm/api/v1/cpPurchaseRequestDtl/customPage"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '10',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{"id":"requestDetailStatus100",'
                             '"property":"requestDetailStatus",'
                            '"operator":"in",'
                             '"value":"[%s]"},'
                            '{"id":"status100",'
                             '"property":"status",'
                             '"operator":"in",'
                             '"value":"[%s]"}]' %(detailstatus, status)),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)

    '''采购申请明细查询'''
    def cpdetail_page(self, key, value):
        url = os.environ["host"] + "/srm/api/v1/cpPurchaseRequestDtl/customPage"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '10',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{{"id":"","value":"{}","property":"{}","operator":"like"}},'
                           '{{"id":"requestDetailStatus100",'
                           '"property":"requestDetailStatus",'
                           '"operator":"in",'
                           '"value":"[100,200,300,400,500,600,700,900]"}},'
                           '{{"id":"status100",'
                           '"property":"status",'
                           '"operator":"in",'
                           '"value":"[100,200,300,400]"}}]'.format(value, key)),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)
    '''转交采购员查询'''
    def cpdetail_userpage(self, value):
        url = os.environ["host"] + "/srm/api/v1/sysUser/purchase/page"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '10',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{"id":"","value":"%s","property":"account","operator":"like"},'
                            '{"id":"state1","property":"state","operator":"=","value":1}]' %value),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)
    '''采购员转交'''
    def cpdetail_transfer(self, account):
        url = os.environ["host"] + "/srm/api/v1/cpPurchaseRequestDtl/transfer"
        data = [
                {
                "accsumCode": "",
                "aggregateDemandQty": None,
                "alreadyAllotQty": 0,
                "alreadyOrderQty": 0,
                "alreadyTransferOrderQty": 0,
                "baseUnitCode": "ZHA",
                "baseUnitName": "张",
                "buyerAccount": account,
                "buyerName": "吴茜",
                "canBuyQty": 1,
                "client": "",
                "companyCode": "6100",
                "companyName": "板式家具公司",
                "conditionalTypeCode": "",
                "costControlDomain": "",
                "cpPurchaseRequestCreateBy": "",
                "createBy": "zhongzijian",
                "createTime": "2021-04-20 10:54:10",
                "currentStatus": None,
                "deliveryAddress": "",
                "demandDate": "2021-04-20 10:54:10",
                "demandName": "",
                "demandQty": 1,
                "demandTrackingNo": "",
                "fixedAssetsCode": "",
                "fixedAssetsName": "",
                "guestListNo": "",
                "isPrice": "1",
                "isQuota": "",
                "lastUpdateBy": "",
                "lastUpdateTime": None,
                "materialCode": "101000007",
                "materialGroupCode": "RA010105",
                "materialGroupName": "原材料/板材/中纤板/12mm中纤板",
                "materialName": "12mm中纤板2440*1220mm",
                "minOrderQty": None,
                "minPackagingQty": None,
                "netDemandQty": None,
                "objectVersionNumber": None,
                "onOrderQty": None,
                "orderPlaceOrderQty": None,
                "planDeliveryDate": "2030-12-30 00:00:00",
                "plantCode": "6199",
                "plantName": "板式家具供应工厂",
                "productionOrder": "",
                "profitCenter": "",
                "projectText": "",
                "purchaseGroupCode": "A01",
                "purchaseGroupName": "板材采购组",
                "purchaseOrgCode": "1000",
                "purchaseOrgName": "",
                "purchaseRequestId": "09b10f42-bdfe-4e5f-b10f-42bdfe8e5f19",
                "purchaseRequestNo": "PR2021042000011",
                "reason": "",
                "remark": "",
                "requestDetailId": "c05f8f7d-4cc0-600a-e053-e8031eac2201",
                "requestDetailRemark": "自动化导入",
                "requestDetailState": 1,
                "requestDetailStatus": 100,
                "requisitionPlantCode": "6110",
                "requisitionPlantName": "板式家具二分厂",
                "requisitioner": "",
                "rowId": "1",
                "rowids": 10,
                "rownum": "",
                "safeStockQty": None,
                "salesOrderDeliveryLine": "",
                "salesOrderLine": "",
                "salesOrderNo": "",
                "state": 1,
                "status": 200,
                "stockQty": None,
                "storageLocationCode": "R19Z",
                "storageLocationName": "六分厂油漆借料库位",
                "storeAddress": "",
                "threeMonthOutStockQty": None,
                "transferQty": None,
                "vendorCode": "700615",
                "vendorName": "测试供应商101",
                "keyIndex": 0
                }
                ]
        return self.s.post(url, json=data)
    '''采购申请明细导出'''
    def cpdetail_report(self):
        url = os.environ["host"] + "/srm-export/api/v1/cpPurchaseRequestDtl/reportExcel"
        webforms = MultipartEncoder(fields=[
            ("filtersRaw", '[{"id":"","value":"PR2021041900040","property":"purchaseRequestNo","operator":"like"},'
                           '{"id":"status100","property":"status","operator":"in","value":"[100,200,400],'
                           '{"id":"requestDetailStatus100","property":"requestDetailStatus","operator":"in","value":"[100]"}]' ),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)
    '''采购申请查看-获取供应商接口'''
    def cpselect_vendor(self):
        url = os.environ["host"] + "/srm/api/v1/vendorMasterData/master/select"
        return self.s.get(url)
    '''采购申请查看-获取公司接口'''
    def cpselect_baseCompany(self):
        url = os.environ["host"] + "/srm/api/v1/baseCompany/spinner"
        return self.s.post(url)
    '''采购申请查看-获取采购员接口'''
    def cpselect_sysUser(self):
        url = os.environ["host"] + "/srm/api/v1/sysUser/purchase/spinner"
        return self.s.post(url)
    '''采购申请查看-获取主单接口'''
    def cpselect_main(self):
        url = os.environ["host"] + "/srm/api/v1/cpPurchaseRequest/editDispose/8e926428-c823-418d-9264-28c823a18d03"
        return self.s.get(url)
    '''采购申请查看-获取明细接口'''
    def cpselect_temp(self):
        url = os.environ["host"] + "/srm/api/v1/cpPurchaseRequestDtlTemp/page"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '20',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw",'[{"id":"tempId","property":"temp_id","operator":"=","value":"8e926428-c823-418d-9264-28c823a18d03"}]'),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)
    '''采购申请查看-获取日志接口'''
    def cpselect_log(self):
        url = os.environ['host'] + "/srm/api/v1/sysBusLog/queryByBusId?busId=8e926428-c823-418d-9264-28c823a18d03&busCreateTime=2021-04-21+11:05:22"
        return self.s.get(url)
    '''采购申请状态查询'''
    def cp_statuspage(self, syncstatus, status):
        url = os.environ["host"] + "/srm/api/v1/cpPurchaseRequest/page"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '10',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{"id":"syncStatus100",'
                             '"property":"syncStatus",'
                            '"operator":"in",'
                             '"value":"%s"},'
                            '{"id":"status200",'
                             '"property":"status",'
                             '"operator":"in",'
                             '"value":"%s"}]' %(syncstatus, status)),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)
    '''配额超标审核记录状态查询'''
    def cp_examineRecordsPage(self, status):
        url = os.environ["host"] + "/srm/api/v1/cpPurchaseRequestOverproof/customRecordPage"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '10',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{"id":"status100","property":"status","operator":"in","value":"[%s]"}]' %status),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)
    '''配额超标审核记录查询'''
    def cp_examineRecordsPg(self, key, value):
        url = os.environ["host"] + "/srm/api/v1/cpPurchaseRequestOverproof/customRecordPage"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '10',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw",'[{"id":"","value":"%s","property":"%s","operator":"like"},'
                          '{"id":"status100","property":"status","operator":"in","value":"[100,200,300]"}]'%(value, key)),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)

    '''采购申请转单状态查询'''
    def cp_zdstatusPage(self, key, status):
        url = os.environ["host"] + "/srm/api/v1/cpPurchaseRequestDtlAllot/customPage"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '1',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{"id":"%s","property":"requestDetailStatus","operator":"in","value":"[%s]"}]' % (key,status)),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)
    '''采购申请转单查询'''
    def cp_zdpage(self, key, value):
        url = os.environ["host"] + "/srm/api/v1/cpPurchaseRequestDtlAllot/customPage"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '5',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw",'[{"id":"","value":"%s","property":"%s","operator":"like"},'
                          '{"id":"requestDetailStatus100","property":"requestDetailStatus","operator":"in",'
                          '"value":"[100]"}]' % (value, key)),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)
    '''采购申请明细分配查询'''
    def cp_zdqueryAllpage(self):
        url = os.environ['host'] + "/srm/api/v1/cpPurchaseRequestDtlAllot/queryAll"
        return self.s.post(url)
    '''采购申请转单分配数量'''
    def cp_zdallotDty(self, Requestid, Detailid):
        url = os.environ['host'] + "/srm/api/v1/cpPurchaseRequestDtlAllot/allotDty"
        data = [
                {
                "accsumCode": "",
                "aggregateDemandQty": None,
                "alreadyAllotQty": 0,
                "alreadyOrderQty": 0,
                "alreadyTransferOrderQty": 0,
                "baseUnitCode": "ZHA",
                "baseUnitName": "张",
                "buyerAccount": "zhongzijian",
                "buyerName": "钟子鉴",
                "canBuyQty": 1,
                "client": "",
                "companyCode": "6100",
                "companyName": "板式家具公司",
                "conditionalTypeCode": "",
                "costControlDomain": "",
                "cpPurchaseRequestCreateBy": "zhongzijian",
                "createBy": "zhongzijian",
                "createTime": "2021-04-21 17:36:58",
                "currentStatus": None,
                "deliveryAddress": "",
                "demandDate": "2021-04-21 17:36:58",
                "demandName": "",
                "demandQty": 1,
                "demandTrackingNo": "",
                "fixedAssetsCode": "",
                "fixedAssetsName": "",
                "guestListNo": "",
                "isPrice": "1",
                "isQuota": "1",
                "lastUpdateBy": "",
                "lastUpdateTime": None,
                "materialCode": "101000007",
                "materialGroupCode": "RA010105",
                "materialGroupName": "原材料/板材/中纤板/12mm中纤板",
                "materialName": "12mm中纤板2440*1220mm",
                "minOrderQty": None,
                "minPackagingQty": None,
                "netDemandQty": None,
                "objectVersionNumber": None,
                "onOrderQty": None,
                "orderPlaceOrderQty": 0,
                "planDeliveryDate": "2030-12-30 00:00:00",
                "plantCode": "6199",
                "plantName": "板式家具供应工厂",
                "productionOrder": "",
                "profitCenter": "",
                "projectText": "",
                "purchaseGroupCode": "A01",
                "purchaseGroupName": "板材采购组",
                "purchaseOrgCode": "1000",
                "purchaseOrgName": "",
                "purchaseRequestId":Requestid,
                "purchaseRequestNo": "PR2021042100017",
                "reason": "",
                "remark": "",
                "requestDetailId": Detailid,
                "requestDetailRemark": "自动化导入",
                "requestDetailState": 1,
                "requestDetailStatus": 100,
                "requisitionPlantCode": "6110",
                "requisitionPlantName": "板式家具二分厂",
                "requisitioner": "",
                "rowId": "1",
                "rowids": 10,
                "rownum": "",
                "safeStockQty": None,
                "salesOrderDeliveryLine": "",
                "salesOrderLine": "",
                "salesOrderNo": "",
                "state": 1,
                "status": 200,
                "stockQty": None,
                "storageLocationCode": "R19Z",
                "storageLocationName": "六分厂油漆借料库位",
                "storeAddress": "",
                "threeMonthOutStockQty": None,
                "transferQty": 1,
                "vendorCode": "700615",
                "vendorName": "测试供应商101",
                "keyIndex": 0
                }
                ]
        return self.s.post(url, json=data)
    '''采购申请转单提交'''
    def cp_zdcommit(self, Requestid, Detailid, Alloid):
        url = os.environ["host"] + "/srm/api/v1/cpPurchaseRequestDtlAllot/commit"
        data = [
                {
                    "allExtraAttributesBaseId": "aaf19f26-cdd6-e9e4-e053-44031eac0fae",
                    "allotQty": 1,
                    "alreadyCancelQty": 0,
                    "billingRatio": None,
                    "conversionPrice": None,
                    "createBy": "zhongzijian",
                    "createTime": "2021-04-23 17:49:56",
                    "fileGroupCode": "",
                    "isOverproof": None,
                    "lastUpdateBy": "",
                    "lastUpdateTime": None,
                    "materialCode": "101000007",
                    "materialGroupCode": "RA010105",
                    "materialName": "12mm中纤板2440*1220mm",
                    "overproofRemark": "",
                    "plantCode": "6199",
                    "price": None,
                    "priceMasterDetailId": "",
                    "priceUnit": None,
                    "purchaseOrgCode": "1000",
                    "purchaseOrgName": "采购供应部",
                    "purchaseRequestAllotId": Alloid,
                    "purchaseRequestDetailId": Detailid,
                    "purchaseRequestId": Requestid,
                    "purchaseRequestNo": "PR2021042200007",
                    "quotaDetailId": "3b8a7901-0e41-422e-8a79-010e41020839",
                    "quotaNumber": 1,
                    "quotaRatio": 100,
                    "state": 1,
                    "status": 100,
                    "transferQty": 1,
                    "vendorCode": "500973",
                    "vendorName": "TCL华瑞照明科技（惠州）有限公司"
                }
                ]
        return self.s.post(url, json=data)

    '''采购申请转单多条提交(超标审核前置)'''
    def cp_zdcomits(self, Requestid, Detailid, Alloid):
        url = os.environ["host"] + "/srm/api/v1/cpPurchaseRequestDtlAllot/commit"
        data = [
    {
        "allExtraAttributesBaseId": "aaf19f26-cdd6-e9e4-e053-44031eac0fae",
        "allotQty": 401,
        "alreadyCancelQty": 0,
        "billingRatio": 100,
        "conversionPrice": 12,
        "createBy": "zhongzijian",
        "createTime": "2021-04-28 14:02:42",
        "fileGroupCode": "",
        "isOverproof": None,
        "lastUpdateBy": "",
        "lastUpdateTime": None,
        "materialCode": "105000007",
        "materialGroupCode": "RA050101",
        "materialName": "直径16黑色圆扣",
        "overproofRemark": "",
        "plantCode": "6199",
        "price": 12,
        "priceMasterDetailId": "1f204afe-db49-453f-a04a-fedb49f53f7e",
        "priceUnit": 1,
        "purchaseOrgCode": "1000",
        "purchaseOrgName": "采购供应部",
        "purchaseRequestAllotId": Alloid,
        "purchaseRequestDetailId": Detailid,
        "purchaseRequestId": Requestid,
        "purchaseRequestNo": "PR2021042800006",
        "quotaDetailId": "efb32b94-fb74-4df8-b32b-94fb74edf8f1",
        "quotaNumber": 241,
        "quotaRatio": 60,
        "state": 1,
        "status": 100,
        "transferQty": 0,
        "vendorCode": "103455",
        "vendorName": "四川万潮科技有限公司"
    },
    {
        "allExtraAttributesBaseId": "aaf19f26-cdd6-e9e4-e053-44031eac0fae",
        "allotQty": 401,
        "alreadyCancelQty": 0,
        "billingRatio": 100,
        "conversionPrice": 10,
        "createBy": "zhongzijian",
        "createTime": "2021-04-28 14:02:42",
        "fileGroupCode": "",
        "isOverproof": None,
        "lastUpdateBy": "",
        "lastUpdateTime": None,
        "materialCode": "105000007",
        "materialGroupCode": "RA050101",
        "materialName": "直径16黑色圆扣",
        "overproofRemark": "",
        "plantCode": "6199",
        "price": 10,
        "priceMasterDetailId": "14faf359-caa8-4f31-baf3-59caa8df31fe",
        "priceUnit": 1,
        "purchaseOrgCode": "1000",
        "purchaseOrgName": "采购供应部",
        "purchaseRequestAllotId": Alloid,
        "purchaseRequestDetailId": Detailid,
        "purchaseRequestId": Requestid,
        "purchaseRequestNo": "PR2021042800006",
        "quotaDetailId": "d65991da-884c-42e5-9991-da884cc2e568",
        "quotaNumber": 160,
        "quotaRatio": 40,
        "state": 1,
        "status": 100,
        "transferQty": "401",
        "vendorCode": "500973",
        "vendorName": "TCL华瑞照明科技（惠州）有限公司"
    }
]
        return self.s.post(url, json=data)

    '''采购申请转单建立提交'''
    def cp_zdjlcommit(self, Tranceid, Detailid, Allotid):
        url = os.environ['host'] + "/srm/api/v1/cpPurchaseRequestTransfer/commit"
        data = {
             "dtos": [
                    {
                        "accsumCode": "",
                        "aggregateDemandQty": None,
                        "allExtraAttributes": "无",
                        "allExtraAttributesBaseId": "aaf19f26-cdd6-e9e4-e053-44031eac0fae",
                        "baseUnitCode": "ZHA",
                        "baseUnitName": "张",
                        "batchFlag": "5e6d14a1-aed3-40ad-ad14-a1aed340adee",
                        "billingRatio": None,
                        "client": "",
                        "companyCode": "6100",
                        "companyName": "板式家具公司",
                        "conversionPrice": None,
                        "costControlDomain": "",
                        "cpPurchaseRequestDtlExtras": "",
                        "deliveryAddress": "",
                        "deliveryAddressCode": "",
                        "demandName": "",
                        "demandQty": 1,
                        "demandTrackingNo": "",
                        "excessDeliveryLimit": None,
                        "fileGroupCode": "",
                        "fixedAssetsCode": "",
                        "fixedAssetsName": "",
                        "floatingRatio": None,
                        "guestListNo": "",
                        "inquiryBillNo": "",
                        "ladderId": "",
                        "materialCode": "101000007",
                        "materialGroupCode": "RA010105",
                        "materialGroupName": "原材料/板材/中纤板/12mm中纤板",
                        "materialName": "12mm中纤板2440*1220mm",
                        "minOrderQty": None,
                        "minPackagingQty": None,
                        "netDemandQty": None,
                        "onOrderQty": None,
                        "overproofRemark": "",
                        "planDeliveryDate": "2030-12-30 00:00:00",
                        "plantCode": "6199",
                        "plantName": "板式家具供应工厂",
                        "price": None,
                        "priceUnit": None,
                        "pricingBillDetailId": "",
                        "pricingBillNo": "",
                        "pricingUnitCode": "",
                        "pricingUnitName": "",
                        "productionOrder": "",
                        "profitCenter": "",
                        "projectText": "",
                        "purchaseGroupCode": "A01",
                        "purchaseGroupName": "板材采购组",
                        "purchaseOrgCode": "1000",
                        "purchaseOrgName": "采购供应部",
                        "purchaseRequestDtlRemark": "自动化导入",
                        "purchaseRequestNo": "PR2021042100004",
                        "quotaQty": 1,
                        "quotaRatio": 100,
                        "remark": "自动化导入",
                        "requestAllotId": Allotid,
                        "requestDetailId": Detailid,
                        "requestTransferId": Tranceid,
                        "requisitionPlantCode": "6110",
                        "requisitionPlantName": "板式家具二分厂",
                        "requisitioner": "",
                        "rowids": 10,
                        "safeStockQty": None,
                        "salesOrderDeliveryLine": "",
                        "salesOrderLine": "",
                        "salesOrderNo": "",
                        "sapDemandQty": None,
                        "shortageOfDelivery": None,
                        "state": 1,
                        "status": 200,
                        "stockQty": None,
                        "storageLocationCode": "R19Z",
                        "storageLocationName": "六分厂油漆借料库位",
                        "storeAddress": "",
                        "threeMonthOutStockQty": None,
                        "transferOrderQty": 1,
                        "vendorCode": "500973",
                        "vendorName": "TCL华瑞照明科技（惠州）有限公司"
                    }
                ]
            }
        return self.s.post(url, json=data)
    '''采购申请转单建成后提交'''
    def cp_cgsqjccommit(self, tempId, bool):
        url = os.environ['host'] + '/srm/api/v1/cpPurchaseOrder'
        data = {
                "absolutePath": "",
                "buyerAccount": "zhongzijian",
                "buyerName": "钟子鉴",
                "companyCode": "6100",
                "companyName": "板式家具公司",
                "createBy": "",
                "createTime": None,
                "currencyCode": "RMB",
                "currencyName": "",
                "dataSource": 1,
                "deliveryDate": "2021-04-26",
                "dtlDTOS": [],
                "exchangeRate": 1,
                "fileGroupCode": "",
                "fileName": "",
                "fileType": "",
                "isAllowedModifyPrice": 1,
                "isFirstSync": None,
                "isTentativeEstimation": 1,
                "isTurnNormal": None,
                "lastAuditTime": None,
                "lastUpdateBy": "",
                "lastUpdateTime": None,
                "objectVersionNumber": None,
                "orderAmount": 6,
                "orderDate": "2021-04-26",
                "orderDtlInputTempDTOList": [],
                "orderReleaseTime": None,
                "purchaseGroupCode": "A01",
                "purchaseGroupName": "板材采购组",
                "purchaseOrderId": "",
                "purchaseOrderNo": "",
                "purchaseOrderTypeCode": "CG07",
                "purchaseOrderTypeName": "采购供应部材料采购订单(价格暂估)",
                "purchaseOrgCode": "1000",
                "purchaseOrgName": "采购供应部",
                "reason": "",
                "remark": "自动化采购转单流程",
                "state": "",
                "status": "",
                "submitFlag": bool,
                "syncMessage": "",
                "syncStatus": "",
                "tempId": tempId,
                "vendorAcceptTime": None,
                "vendorCode": "500973",
                "vendorName": "TCL华瑞照明科技（惠州）有限公司"
            }
        return self.s.post(url, json=data)
    '''采购订单管理查询'''
    def cp_orderpage(self, key, value):
        url = os.environ['host'] + '/srm/api/v1/cpPurchaseOrder/page'
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '1',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw",'[{"id":"","value":"%s","property":"%s","operator":"like"},'
                          '{"id":"status100","property":"status","operator":"in","value":"[100,101,102,200,300,400,500,600]"},'
                          '{"id":"syncStatus100","property":"syncStatus","operator":"in","value":"[100,200,300,400,500]"}]' % (value, key)),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)
    '''根据公司查可提交明细'''
    def cp_queryByCompanyVendor(self,vendorCode ,companyCode, purchaseGroupCode):
        url = os.environ['host'] + "/srm/api/v1/cpPurchaseRequestTransfer/queryByCompanyVendor"
        data = {"vendorCode":vendorCode,"companyCode":companyCode,"purchaseGroupCode":purchaseGroupCode,"salesOrderNo":"","batchFlag":""}
        return self.s.post(url, json=data)

    '''获取采购订单明细'''
    def cp_ordertempPage(self, tempid):
        url = os.environ['host'] + '/srm/api/v1/cpPurchaseOrderDtl/tempPage/%s' % tempid
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '5',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[]'),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)
    '''采购订单明细编辑'''
    def cp_orderDetailEdit(self, tempid, detailtempid, Tranceid, orderdetailid):
        url = os.environ["host"] + "/srm/api/v1/cpPurchaseOrderDtl"
        data = {
                "accsumCode": "",
                "aggregateDemandQty": None,
                "allExtraAttributes": "无",
                "allExtraAttributesBaseId": "aaf19f26-cdd6-e9e4-e053-44031eac0fae",
                "alreadyDeliveryQty": 0,
                "alreadyReceivingQty": 0,
                "area": None,
                "baseUnitCode": "ZHA",
                "baseUnitName": "张",
                "billingRatio": 0,
                "calculateFormula": "",
                "client": "",
                "conditionalTypeCode": "总价格",
                "contractNo": "",
                "conventDenominator": None,
                "conventDenominator1": 1,
                "conventDenominator2": 1,
                "conventNumerator": None,
                "conventNumerator1": 1,
                "conventNumerator2": 1,
                "costCenter": "",
                "costControlDomain": "",
                "cpPurchaseOrderDTO": {
                    "absolutePath": "",
                    "buyerAccount": "zhongzijian",
                    "buyerName": "钟子鉴",
                    "companyCode": "6100",
                    "companyName": "板式家具公司",
                    "createBy": "",
                    "createTime": None,
                    "currencyCode": "RMB",
                    "currencyName": "",
                    "dataSource": 1,
                    "deliveryDate": "2021-04-26",
                    "dtlDTOS": [],
                    "exchangeRate": 1,
                    "fileGroupCode": "",
                    "fileName": "",
                    "fileType": "",
                    "isAllowedModifyPrice": 1,
                    "isFirstSync": None,
                    "isTentativeEstimation": 1,
                    "isTurnNormal": None,
                    "lastAuditTime": None,
                    "lastUpdateBy": "",
                    "lastUpdateTime": None,
                    "objectVersionNumber": None,
                    "orderAmount": 10,
                    "orderDate": "2021-04-26",
                    "orderDtlInputTempDTOList": [],
                    "orderReleaseTime": None,
                    "purchaseGroupCode": "A01",
                    "purchaseGroupName": "板材采购组",
                    "purchaseOrderId": "",
                    "purchaseOrderNo": "",
                    "purchaseOrderTypeCode": "CG07",
                    "purchaseOrderTypeName": "采购供应部材料采购订单(价格暂估)",
                    "purchaseOrgCode": "1000",
                    "purchaseOrgName": "采购供应部",
                    "reason": "",
                    "remark": "",
                    "state": None,
                    "status": None,
                    "submitFlag": True,
                    "syncMessage": "",
                    "syncStatus": None,
                    "tempId": tempid,
                    "vendorAcceptTime": None,
                    "vendorCode": "500973",
                    "vendorName": "TCL华瑞照明科技（惠州）有限公司"
                },
                "createBy": "zhongzijian",
                "createTime": "2021-04-26 16:23:47",
                "dataSource": 1,
                "deliveryAddress": "",
                "deliveryDate": "2021-04-26",
                "demandName": "",
                "demandTrackingNo": "",
                "detailTempId": detailtempid,
                "excessDeliveryLimit": None,
                "fixedAssetsCode": "",
                "fixedAssetsName": "",
                "floatingRatio": None,
                "guestListNo": "",
                "hasData": None,
                "height": None,
                "inquiryBillNo": "",
                "isFree": 0,
                "isFreeCode": None,
                "isNeedSyncSap": 1,
                "isOrderReceiving": 0,
                "isOrderReceivingCode": None,
                "isQualityTesting": 1,
                "isQualityTestingCode": None,
                "isReturn": 0,
                "isReturnCode": None,
                "isSchedule": 1,
                "isScheduleCode": None,
                "ladderId": "",
                "lastUpdateBy": "zhongzijian",
                "lastUpdateTime": "2021-04-26 16:33:50",
                "lengths": None,
                "lineAmount": 1,
                "lineItemTypeCode": "-1",
                "lineItemTypeName": "标准",
                "materialCode": "101000007",
                "materialGroupCode": "RA010105",
                "materialGroupName": "原材料/板材/中纤板/12mm中纤板",
                "materialIds": [],
                "materialName": "12mm中纤板2440*1220mm",
                "minOrderQty": None,
                "minPackagingQty": None,
                "netDemandQty": None,
                "objectVersionNumber": None,
                "oldOrderQty": None,
                "onOrderQty": None,
                "orderDetailId": orderdetailid,
                "orderModifyReason": "",
                "orderQty": 1,
                "orderUnitCode": "ZHA",
                "orderUnitName": "张",
                "originalPrice": 10,
                "planDeliveryDays": 0,
                "plantCode": "6199",
                "plantName": "板式家具供应工厂",
                "price": "1",
                "priceMasterDetailIds": [],
                "priceUnit": 1,
                "pricingBillDetailId": "",
                "pricingBillNo": "",
                "pricingUnitCode": "ZHA",
                "pricingUnitName": "张",
                "productionOrder": "",
                "profitCenter": "",
                "projectText": "",
                "purchaseOrderExtraTempList": [
                    {
                        "categoryCode": "default",
                        "categoryId": "aaf18978-8dbd-e860-e053-44031eac1ca4",
                        "categoryName": "默认扩展类别",
                        "createBy": "zhongzijian",
                        "createTime": "2021-04-26 16:23:47",
                        "detailTempId": detailtempid,
                        "extraAttributesBaseId": "aaf19f26-cdd6-e9e4-e053-44031eac0fae",
                        "extraAttributesCode": "default",
                        "extraAttributesName": "无扩展属性",
                        "extraId": "1b931290-1d34-44f3-9312-901d34b4f310",
                        "extraTempId": "cab711c2-f502-4a3e-b711-c2f502ca3eb2",
                        "lastUpdateBy": "",
                        "lastUpdateTime": None,
                        "objectVersionNumber": None,
                        "orderDetailId": "c8d73477-f061-41df-9734-77f061c1df27",
                        "remark": "",
                        "state": 3,
                        "tempId": tempid,
                        "type": "子"
                    }
                ],
                "purchaseOrderId": tempid,
                "purchaseRequestNo": "PR2021041700001",
                "purchaseUnitCode": "ZHA",
                "purchaseUnitId": "ba30d8f0-6e7b-1579-e053-980d1fac919f",
                "purchaseUnitName": "张",
                "realCalculateFormula": "",
                "remark": "自动化导入",
                "requestCanOrderQty": None,
                "requestDemandQty": 1,
                "requestDetailId": "c0278de3-15a7-031c-e053-e8031eaccba7",
                "requestDetailIds": [],
                "requestNumber": "",
                "requestRowids": None,
                "requestTransferId": Tranceid,
                "requisitionPlantCode": "6110",
                "requisitionPlantName": "板式家具二分厂",
                "requisitioner": "",
                "rowids": 10,
                "safeStockQty": None,
                "salesOrderDeliveryLine": "",
                "salesOrderLine": "",
                "salesOrderNo": "",
                "sapDemandQty": None,
                "shortageOfDelivery": None,
                "state": 3,
                "status": 100,
                "stockQty": None,
                "storageLocationCode": "R19Z",
                "storageLocationName": "六分厂油漆借料库位",
                "storeAddress": "",
                "subjectAssignTypeCode": " ",
                "subjectAssignTypeName": "",
                "tempId": tempid,
                "threeMonthOutStockQty": None,
                "vendorAddress": "广东省惠州市仲恺高新区惠风四路72号",
                "vendorPostalCode": "516006",
                "width": None,
                "keyIndex": 0,
                "orderUnitList": [
                    {
                        "orderUnitCode": "ZHA",
                        "orderUnitName": "张"
                    }
                ],
                "plantList": [
                    {
                        "companyCode": "6100",
                        "companyId": "34f63026-8f2d-4f49-b630-268f2d6f4001",
                        "companyName": "板式家具公司",
                        "createBy": "wuxi",
                        "createTime": "2020-07-03 09:36:00",
                        "lastUpdateBy": "SAP",
                        "lastUpdateTime": "2020-11-27 17:56:11",
                        "objectVersionNumber": None,
                        "plantCode": "6199",
                        "plantId": "af758aca-a847-41c5-b58a-caa847d1c568",
                        "plantName": "板式家具供应工厂",
                        "purchaseGroupCode": "A01",
                        "purchaseGroupId": "843a0c2a-7ef1-42fb-ba0c-2a7ef1900034",
                        "purchaseGroupName": "板材采购组",
                        "purchaseOrgCode": "",
                        "purchaseOrgId": "4eb74245-e975-4cd1-b742-45e975ccd1a1",
                        "purchaseOrgName": "",
                        "reason": "",
                        "state": 1
                    }
                ]
            }
        return self.s.put(url, json=data)
    '''供应商引入状态查询'''
    def vendorImport(self, source, status):
        url = os.environ["host"] + "/srm/api/v1/vendorImport/page"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '1',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{"id":"source1","property":"source","operator":"in","value":"%s1"},'
                           '{"id":"status100","property":"status","operator":"in",'
                           '"value":"%s2"}]' % (source, status)),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)
    '''供应商主数据数据状态查询'''
    def vendorMasterData_master_page(self, state):
        url = os.environ["host"] + "/srm/api/v1/vendorMasterData/master/page"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '1',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{"id":"state1","property":"state","operator":"in","value":"%s"}]' % state),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)
    '''供应商信息变更管理状态'''
    def vendorChangeInfo_page(self, status):
        url = os.environ["host"] + "/srm/api/v1/vendorChangeInfo/page"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '1',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{"id":"status100","property":"status","operator":"in","value":"%s"}]' % status),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)
    '''采购申请明细取消分配'''
    def cp_zdcacle(self, Alloid, Requestid, Detailid, No):
        url = os.environ['host'] + '/srm/api/v1/cpPurchaseRequestDtlAllot/cancel'
        data = [
            {
                "allExtraAttributesBaseId": "aaf19f26-cdd6-e9e4-e053-44031eac0fae",
                "allotQty": 1,
                "alreadyCancelQty": 0,
                "billingRatio": None,
                "conversionPrice": None,
                "createBy": "zhongzijian",
                "createTime": "2021-04-27 14:14:22",
                "fileGroupCode": "",
                "isOverproof": None,
                "lastUpdateBy": "",
                "lastUpdateTime": None,
                "materialCode": "101000001",
                "materialGroupCode": "RA010101",
                "materialName": "3mm中纤板2440*1220mm",
                "overproofRemark": "",
                "plantCode": "6199",
                "price": None,
                "priceMasterDetailId": "",
                "priceUnit": None,
                "purchaseOrgCode": "1000",
                "purchaseOrgName": "采购供应部",
                "purchaseRequestAllotId": Alloid,
                "purchaseRequestDetailId": Detailid,
                "purchaseRequestId": Requestid,
                "purchaseRequestNo": No,
                "quotaDetailId": "c0b5a456-638e-43a5-b5a4-56638ec3a55c",
                "quotaNumber": 1,
                "quotaRatio": 100,
                "state": 1,
                "status": 100,
                "transferQty": 1,
                "vendorCode": "700615",
                "vendorName": "测试供应商101"
            }
        ]
        return self.s.post(url, json=data)
    '''采购申请转单取消'''
    def cpPurchase_cancel(self, batchFlag, TransferId):
        url = os.environ['host'] + "/srm/api/v1/cpPurchaseRequestTransfer/cancel"
        data = [
    {
        "accsumCode": "",
        "aggregateDemandQty": None,
        "allExtraAttributes": "无",
        "allExtraAttributesBaseId": "aaf19f26-cdd6-e9e4-e053-44031eac0fae",
        "baseUnitCode": "ZHA",
        "baseUnitName": "张",
        "batchFlag": batchFlag,
        "billingRatio": None,
        "client": "",
        "companyCode": "6100",
        "companyName": "板式家具公司",
        "conversionPrice": None,
        "costControlDomain": "",
        "cpPurchaseRequestDtlExtras": [],
        "deliveryAddress": "",
        "deliveryAddressCode": "",
        "demandName": "",
        "demandQty": 1000,
        "demandTrackingNo": "11111",
        "excessDeliveryLimit": None,
        "fileGroupCode": "",
        "fixedAssetsCode": "",
        "fixedAssetsName": "",
        "floatingRatio": None,
        "guestListNo": "",
        "inquiryBillNo": "",
        "ladderId": "",
        "materialCode": "101000021",
        "materialGroupCode": "RA010108",
        "materialGroupName": "原材料/板材/中纤板/25mm中纤板",
        "materialName": "25mm中纤板2440*1220mm",
        "minOrderQty": None,
        "minPackagingQty": None,
        "netDemandQty": None,
        "onOrderQty": None,
        "overproofRemark": "自动化取消",
        "planDeliveryDate": "2024-04-01 00:00:00",
        "plantCode": "6199",
        "plantName": "板式家具供应工厂",
        "price": None,
        "priceUnit": None,
        "pricingBillDetailId": "",
        "pricingBillNo": "",
        "pricingUnitCode": "",
        "pricingUnitName": "",
        "productionOrder": "",
        "profitCenter": "",
        "projectText": "",
        "purchaseGroupCode": "A01",
        "purchaseGroupName": "板材采购组",
        "purchaseOrgCode": "1000",
        "purchaseOrgName": "采购供应部",
        "purchaseRequestDtlRemark": "查看接口测试数据",
        "purchaseRequestNo": "PR2021042100008",
        "quotaQty": 1000,
        "quotaRatio": 100,
        "remark": "查看接口测试数据",
        "requestAllotId": "8ce3691f-136f-49c6-a369-1f136ff9c6a0",
        "requestDetailId": "448ad576-bcc5-4689-8ad5-76bcc5d68971",
        "requestTransferId": TransferId,
        "requisitionPlantCode": "6199",
        "requisitionPlantName": "板式家具供应工厂",
        "requisitioner": "贝克",
        "rowids": 10,
        "safeStockQty": None,
        "salesOrderDeliveryLine": "",
        "salesOrderLine": "",
        "salesOrderNo": "",
        "sapDemandQty": None,
        "shortageOfDelivery": None,
        "state": 1,
        "status": 200,
        "stockQty": None,
        "storageLocationCode": "D004",
        "storageLocationName": "三分厂呆滞材料库",
        "storeAddress": "西航港",
        "threeMonthOutStockQty": None,
        "transferOrderQty": 1000,
        "vendorCode": "500973",
        "vendorName": "TCL华瑞照明科技（惠州）有限公司"
    }
]
        return self.s.post(url, json=data)

    '''配额超标审核'''
    def cp_audit(self, auditid, auditFlag):
        url = os.environ['host'] + "/srm/api/v1/cpPurchaseRequestOverproof/audit"
        data = {"ids":[auditid],"auditFlag": auditFlag,"reason":""}
        return self.s.post(url, json=data)

    '''配额超标审核查询'''
    def cp_customPage(self, key, value):
        url = os.environ["host"] + "/srm/api/v1/cpPurchaseRequestOverproof/customPage"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '5',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw",'[{"id":"","value":"%s","property":"%s","operator":"like"}]' % (value, key)),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)

    '''缺料提报状态查询'''
    def cpLackMaterialSub_statusPage(self, key, value):
        url = os.environ["host"] + "/srm/api/v1/cpLackMaterialSub/page"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '5',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{"id":"%s","property":"status","operator":"in","value":"[%s]"}]' % (key, value)),
            ("sortersRaw", '[{"id":"createTime","property":"createTime","direction":"DESC"}]')
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)

    '''缺料提报查询'''
    def cpLackMaterialSub_qlpage(self, key, value):
        url = os.environ["host"] + "/srm/api/v1/cpLackMaterialSub/page"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '5',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{"id":"","value":"%s","property":"%s","operator":"like"},'
                           '{"id":"status100","property":"status","operator":"in","value":"[100,200,300,301,400]"}]'%(value, key)),
            ("sortersRaw", '[{"id":"createTime","property":"createTime","direction":"DESC"}]')
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)

    '''根据公司查询工厂'''
    def basePlant(self):
        url = os.environ['host'] + '/srm/api/v1/basePlant/spinner/6100'
        return self.s.get(url)

    '''根据工厂查询库位'''
    def baseStorageLocation(self):
        url = os.environ['host'] + '/srm/api/v1/baseStorageLocation/storage/af758aca-a847-41c5-b58a-caa847d1c568'
        return self.s.get(url)

    '''根据工厂获取物料'''
    def customByPlantPage(self):
        url = os.environ["host"] + "/srm/api/v1/materialMasterData/customByPlantPage/6199"
        webforms = MultipartEncoder(fields=[
            ("page", '1'),
            ("rows", '5',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{"id":"state1","property":"state","operator":"=","value":1}]')
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)

    '''缺料提报新增'''
    def cpLackMaterialSub_add(self, processamento):
        remark = uuid.uuid4()
        url = os.environ["host"] + "/srm/api/v1/cpLackMaterialSub"
        data = {
                "lackMaterialSubId": "",
                "lackMaterialSubNo": "",
                "purchaseRequestNo": "",
                "companyCode": "6100",
                "companyName": "板式家具公司",
                "plantCode": "6199",
                "plantName": "板式家具供应工厂",
                "storageLocationCode": "D004",
                "storageLocationName": "三分厂呆滞材料库",
                "materialGroupCode": "RA050700",
                "materialGroupName": "原材料/五金/铝门框",
                "materialCode": "196335450",
                "materialName": "双面黑色铝框QP-20左开玻璃门窄边框575*332*21(定制)",
                "baseUnitCode": "ZHA",
                "baseUnitName": "张",
                "buyerAccount": "zhongzijian",
                "buyerName": "钟子鉴",
                "processamento": processamento,
                "scheduleDate": "2021-04-01 00:00:00",
                "productionOrderNo": "ci001",
                "productName": "%s"%remark,
                "businessType": "Z01",
                "pickingListNo": "001",
                "demandQty": "1",
                "lackMaterialQty": "1",
                "uncollectedQty": "",
                "subRemark": "自动化新增缺料提报",
                "processingMode": "",
                "expectedArrivalTime": "",
                "confirmRemark": "",
                "arrivalQty": "",
                "warehouseArrivalTime": "",
                "receivingRemark": "",
                "submitFlag": True
            }
        r = self.s.post(url, json=data)
        return r,remark
    '''缺料提报保存'''
    def cpLackMaterialSub_Save(self, processamento):
        remark = uuid.uuid4()
        url = os.environ["host"] + "/srm/api/v1/cpLackMaterialSub"
        data = {
                "lackMaterialSubId": "",
                "lackMaterialSubNo": "",
                "purchaseRequestNo": "",
                "companyCode": "6100",
                "companyName": "板式家具公司",
                "plantCode": "6199",
                "plantName": "板式家具供应工厂",
                "storageLocationCode": "D004",
                "storageLocationName": "三分厂呆滞材料库",
                "materialGroupCode": "RA100100",
                "materialGroupName": "原材料/样品材料/套房类样品材料",
                "materialCode": "110039895",
                "materialName": "样品200206电视柜台面岩板2101*365*6",
                "baseUnitCode": "ZHA",
                "baseUnitName": "张",
                "buyerAccount": "zhongzijian",
                "buyerName": "钟子鉴",
                "processamento": processamento,
                "scheduleDate": "2021-04-01 00:00:00",
                "productionOrderNo": "saveci001",
                "productName": "%s"%remark,
                "businessType": "Z01",
                "pickingListNo": "1",
                "demandQty": "1",
                "lackMaterialQty": "1",
                "uncollectedQty": "",
                "subRemark": "自动化保存测试",
                "processingMode": "",
                "expectedArrivalTime": "",
                "confirmRemark": "",
                "arrivalQty": "",
                "warehouseArrivalTime": "",
                "receivingRemark": "",
                "submitFlag": False
            }
        r = self.s.post(url, json=data)
        return r, remark

    '''缺料提报编辑保存'''
    def cpLackMaterialSub_EditSave(self,processamento):
        url = os.environ["host"] + "/srm/api/v1/cpLackMaterialSub"
        data= {
                "arrivalQty": None,
                "baseUnitCode": "ZHA",
                "baseUnitName": "张",
                "businessType": "Z01",
                "buyerAccount": "zhongzijian",
                "buyerName": "钟子鉴",
                "companyCode": "6100",
                "companyName": "板式家具公司",
                "confirmRemark": "",
                "createBy": "zhongzijian",
                "createTime": "2021-04-29 14:38:12",
                "demandQty": 1,
                "expectedArrivalTime": None,
                "lackMaterialQty": 1,
                "lackMaterialSubId": "3e316193-33d7-4dbe-b161-9333d7bdbe2d",
                "lackMaterialSubNo": "",
                "lastUpdateBy": "zhongzijian",
                "lastUpdateTime": "2021-04-29 15:09:36",
                "materialCode": "110039895",
                "materialGroupCode": "RA100100",
                "materialGroupName": "原材料/样品材料/套房类样品材料",
                "materialName": "样品200206电视柜台面岩板2101*365*6",
                "objectVersionNumber": None,
                "pickingListNo": "1",
                "plantCode": "6199",
                "plantName": "板式家具供应工厂",
                "processamento": processamento,
                "processingMode": "",
                "productName": "3e316193-33d7-4dbe-b161",
                "productionOrderNo": "saveci001",
                "purchaseRequestNo": "",
                "receivingRemark": "",
                "scheduleDate": "2021-04-01 00:00:00",
                "state": 1,
                "status": 100,
                "storageLocationCode": "D004",
                "storageLocationName": "三分厂呆滞材料库",
                "subRemark": "自动化保存测试",
                "submitFlag": False,
                "uncollectedQty": 1,
                "warehouseArrivalTime": None,
                "keyIndex": 17
            }
        return self.s.post(url, json=data)

    '''缺料提报编辑提交'''
    def cpLackMaterialSub_EditCommit(self,processamento):
        url = os.environ['host'] + "/srm/api/v1/cpLackMaterialSub"
        data = {
                "arrivalQty": None,
                "baseUnitCode": "ZHA",
                "baseUnitName": "张",
                "businessType": "Z01",
                "buyerAccount": "zhongzijian",
                "buyerName": "钟子鉴",
                "companyCode": "6100",
                "companyName": "板式家具公司",
                "confirmRemark": "",
                "createBy": "zhongzijian",
                "createTime": "2021-04-29 15:02:37",
                "demandQty": 1,
                "expectedArrivalTime": None,
                "lackMaterialQty": 1,
                "lackMaterialSubId": "79bd2b81-4aca-48ac-bd2b-814acaf8acff",
                "lackMaterialSubNo": "",
                "lastUpdateBy": "",
                "lastUpdateTime": None,
                "materialCode": "110039895",
                "materialGroupCode": "RA100100",
                "materialGroupName": "原材料/样品材料/套房类样品材料",
                "materialName": "样品200206电视柜台面岩板2101*365*6",
                "objectVersionNumber": None,
                "pickingListNo": "1",
                "plantCode": "6199",
                "plantName": "板式家具供应工厂",
                "processamento": processamento,
                "processingMode": "",
                "productName": "2d232a1d-82f6-4ba6-9867-4f96b572c7a1",
                "productionOrderNo": "saveci001",
                "purchaseRequestNo": "",
                "receivingRemark": "",
                "scheduleDate": "2021-04-01 00:00:00",
                "state": 1,
                "status": 100,
                "storageLocationCode": "D004",
                "storageLocationName": "三分厂呆滞材料库",
                "subRemark": "自动化编辑提交测试",
                "submitFlag": True,
                "uncollectedQty": 1,
                "warehouseArrivalTime": None,
                "keyIndex": 0
            }
        return self.s.post(url, json=data)

    '''缺料提报删除'''
    def lackMaterial(self, lackMaterialSubId):
        url = os.environ["host"] +"/srm/api/v1/cpLackMaterialSub/lackMaterial"
        data = [
            {
                "arrivalQty": None,
                "baseUnitCode": "ZHA",
                "baseUnitName": "张",
                "businessType": "Z01",
                "buyerAccount": "zhongzijian",
                "buyerName": "钟子鉴",
                "companyCode": "6100",
                "companyName": "板式家具公司",
                "confirmRemark": "",
                "createBy": "zhongzijian",
                "createTime": "2021-04-29 15:02:37",
                "demandQty": 1,
                "expectedArrivalTime": None,
                "lackMaterialQty": 1,
                "lackMaterialSubId": lackMaterialSubId,
                "lackMaterialSubNo": "",
                "lastUpdateBy": "",
                "lastUpdateTime": None,
                "materialCode": "110039895",
                "materialGroupCode": "RA100100",
                "materialGroupName": "原材料/样品材料/套房类样品材料",
                "materialName": "样品200206电视柜台面岩板2101*365*6",
                "objectVersionNumber": None,
                "pickingListNo": "1",
                "plantCode": "6199",
                "plantName": "板式家具供应工厂",
                "processamento": "3",
                "processingMode": "",
                "productName": "e701bccd-16d9-4d4f-ac62-c98b6c279473",
                "productionOrderNo": "saveci001",
                "purchaseRequestNo": "",
                "receivingRemark": "",
                "scheduleDate": "2021-04-01 00:00:00",
                "state": 1,
                "status": 100,
                "storageLocationCode": "D004",
                "storageLocationName": "三分厂呆滞材料库",
                "subRemark": "自动化保存测试",
                "submitFlag": None,
                "uncollectedQty": 1,
                "warehouseArrivalTime": None,
                "keyIndex": 0
            }
        ]
        return self.s.delete(url, json=data)

    '''采购员确认查询'''
    def buyerConfirm_page(self, key, value):
        url = os.environ['host'] +'/srm/api/v1/cpLackMaterialSub/buyerConfirm/page'
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '5',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{"id":"","value":"%s","property":"%s","operator":"like"}]'%(value, key)),
            ("sortersRaw", '[{"id":"createTime","property":"createTime","direction":"DESC"}]')
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)

    '''采购员确认页面转交'''
    def buyerCareOf(self, sysUser, buyerAccount):
        url = os.environ["host"] + "/srm/api/v1/cpLackMaterialSub/buyerCareOf/%s" % sysUser
        data = [
    {
        "arrivalQty": None,
        "baseUnitCode": "ZHA",
        "baseUnitName": "张",
        "businessType": "Z01",
        "buyerAccount": buyerAccount,
        "buyerName": "钟子鉴",
        "companyCode": "6100",
        "companyName": "板式家具公司",
        "confirmRemark": "",
        "createBy": "zhongzijian",
        "createTime": "2021-04-29 11:34:22",
        "demandQty": 1,
        "expectedArrivalTime": None,
        "lackMaterialQty": 1,
        "lackMaterialSubId": "ad828361-eae9-4d53-8283-61eae98d5371",
        "lackMaterialSubNo": "TBD2021042900002",
        "lastUpdateBy": "",
        "lastUpdateTime": None,
        "materialCode": "196335450",
        "materialGroupCode": "RA050700",
        "materialGroupName": "原材料/五金/铝门框",
        "materialName": "双面黑色铝框QP-20左开玻璃门窄边框575*332*21(定制)",
        "objectVersionNumber": None,
        "pickingListNo": "1",
        "plantCode": "6199",
        "plantName": "板式家具供应工厂",
        "processamento": "3",
        "processingMode": "",
        "productName": "1",
        "productionOrderNo": "1",
        "purchaseRequestNo": "",
        "receivingRemark": "",
        "scheduleDate": "2021-04-01 00:00:00",
        "state": 1,
        "status": 200,
        "storageLocationCode": "D004",
        "storageLocationName": "三分厂呆滞材料库",
        "subRemark": "",
        "submitFlag": None,
        "uncollectedQty": 1,
        "warehouseArrivalTime": None,
        "keyIndex": 0
    }
]
        return self.s.post(url, json=data)
