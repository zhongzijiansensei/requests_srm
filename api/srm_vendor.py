import os
import requests
from requests_toolbelt import MultipartEncoder

class Srmvendor(object):
    def __init__(self, s: requests.session):
        self.s = s
    '''供应商查询'''
    def vendorMasterData_page(self, key, value):
        url = os.environ["host"] + "/srm/api/v1/vendorMasterData/master/page"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '20',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{"id":"","value":"%s","property":"%s","operator":"like"},'
                           '{"id":"state1","property":"state","operator":"in","value":"[1]"}]' % (value, key)),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)
    '''新建质量问题查询'''
    def vendorQualityQuestion_page(self, key, value):
        url = os.environ["host"] + "/srm/api/v1/vendorQualityQuestion/page"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '20',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{"id":"","value":"%s","property":"%s","operator":"like"},'
                           '{"id":"status100","property":"status","operator":"in","value":"[100,201]"}]' % (value, key)),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)
    '''新建质量问题保存'''
    def vendorQualityQuestion_save(self, purchasePerson):
        url = os.environ["host"] + "/srm/api/v1/vendorQualityQuestion?nextStatus=QUALITY_WAIT_SUBMIT"
        data = {
                "qualityTroubleNo": "123",
                "troubleType": "1",
                "plantName": "板式家具供应工厂",
                "plantCode": "6199",
                "purchaseOrgCode": "1000",
                "purchaseOrgName": "采购供应部",
                "companyName": "板式家具公司",
                "companyCode": "6100",
                "vendorId": "1160d372-927f-4200-a0d3-72927f72002a",
                "vendorCode": "500969",
                "vendorName": "崇州市鑫鸿鑫曲木家具有限公司",
                "purchasePerson": "[wuxi]吴茜",
                "presentDate": "2021-04-21",
                "remark": "123"
                }
        print(purchasePerson)
        p = self.s.post(url, data=data)
        return p, purchasePerson
    '''新增质量问题提交'''
    def vendorQualityQuestion_add(self, purchasePerson):
        url = os.environ["host"] + "/srm/api/v1/vendorQualityQuestion?nextStatus=FINANCE_WAIT_DEAL"
        data = {
            "qualityTroubleNo": "test123",
            "troubleType": "1",
            "plantName": "板式家具供应工厂",
            "plantCode": "6199",
            "purchaseOrgCode": "1000",
            "purchaseOrgName": "采购供应部",
            "companyName": "板式家具公司",
            "companyCode": "6100",
            "vendorId": "152f3b1f-ce6c-4573-af3b-1fce6c7573c2",
            "vendorCode": "900569",
            "vendorName": "江苏新绿盛环保设备有限公司",
            "purchasePerson": purchasePerson,
            "presentDate": "2021-04-21",
            "remark": "test123"
        }
        print(purchasePerson)
        p = self.s.post(url, data=data)
        return p, purchasePerson
    '''银行信息管理数据查询'''
    def vendorBankInfoManage_page(self, key, value):
        url = os.environ["host"] + "/srm/api/v1/vendorBankInfoManage/page"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '20',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{"id":"","value":"%s","property":"%s","operator":"like"},'
                           '{"id":"bankStatus300","property":"bankStatus","operator":"in","value":"[300]"}]' % (
             value, key)),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)
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
    '''供应商主数据导出'''
    def vendorMasterData_reportExcel(self):
        url = os.environ["host"] + "/srm-export/api/v1/vendorMasterData/reportExcel"
        webforms = MultipartEncoder(fields=[
            ("filtersRaw", '[{"id":"state1","property":"state","operator":"in","value":"[1]"}]'),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)
    '''银行信息管理导出'''
    def vendorBankInfoManage_exportExcle(self):
        url = os.environ["host"] + "/srm-export/api/v1/vendorBankInfoManage/exportExcle"
        webforms = MultipartEncoder(fields=[
            ("filtersRaw", '[{"id":"bankStatus300","property":"bankStatus","operator":"in","value":"[300]"}]'),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)
    '''质量问题管理导出数据接口'''
    def vendorQualityQuestion_export(self):
        url = os.environ["host"] + "/srm-export/api/v1/vendorQualityQuestion/export"
        webforms = MultipartEncoder(fields=[
            ("filtersRaw", '[{"id":"troubleType1","property":"troubleType","operator":"in","value":"[1]"},'
                           '{"id":"status500","property":"status","operator":"in","value":"[500]"}]'),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)

    '''查询银行信息管理状态'''
    def vendorBankInfoManage_page1(self, bankStatus):
        url = os.environ["host"] + "/srm/api/v1/vendorBankInfoManage/page"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '1',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{"id":"bankStatus100","property":"bankStatus","operator":"in","value":"%s"}]' % bankStatus),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)

    '''供应商银行明细信息状态查询'''
    def vendorBankInfoManage_detail_page(self, state, status):
        url = os.environ["host"] + "/srm/api/v1/vendorBankInfoManage/detail/page"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '1',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{"id":"state1","property":"state","operator":"in","value":"%s1"},'
                           '{"id":"status100","property":"status","operator":"in","value":"%s2"}]' % (state, status)),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)

    '''新建质量问题事故类型和状态查询'''
    def vendorQualityQuestion_page1(self, troubleType, status):
        url = os.environ["host"] + "/srm/api/v1/vendorQualityQuestion/page"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '1',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{"id":"troubleType1","property":"troubleType","operator":"in","value":"%s"},'
                           '{"id":"status100","property":"status","operator":"in","value":"%s"}]' % (troubleType, status)),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)

    '''质量问题管理事故类型和状态查询'''
    def vendorQualityQuestion_page2(self, troubleType, status):
        url = os.environ["host"] + "/srm/api/v1/vendorQualityQuestion/page"
        webforms = MultipartEncoder(fields=[
            ("page", '1',),
            ("rows", '1',),
            ("order", 'desc',),
            ("pageFlag", 'true',),
            ("onlyCountFlag", 'false',),
            ("filtersRaw", '[{"id":"troubleType1","property":"troubleType","operator":"in","value":"%s"},'
                           '{"id":"status100","property":"status","operator":"in","value":"%s"}]' % (troubleType, status)),
        ]
        )
        headers = {
            'Content-Type': webforms.content_type,
        }
        return self.s.post(url, headers=headers, data=webforms)