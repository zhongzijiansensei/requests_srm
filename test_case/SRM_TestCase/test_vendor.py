# -*- coding: UTF-8 -*-

import allure
import pytest
from common.logger import Log
from common.read_yaml import ReadYaml
from api.SRM_Base import SRMBase
import jsonpath
# from common.connect_oracle import Db_Oracle


@allure.feature("供应商模块测试")
class TestSrmVendor:
    log = Log()
    testdata = ReadYaml("case_data.yml").get_yaml_data()

    @pytest.mark.prod
    @pytest.mark.parametrize("key,value,expect", testdata["vendorMasterData_page_data"],
                             ids=["供应商编码", "数据状态"])
    @allure.feature('供应商主数据查询')  # 测试报告显示测试功能
    def test_vendorMasterData_page(self, gettokenfixture, key, value, expect):
        s = gettokenfixture
        self.log.info("----供应商主数据查询接口----")
        r = SRMBase(s)
        msg = r.vendorMasterData_page(key, value)
        self.log.info("获取请求结果: %s" % msg.json())
        if key == "vendorCode":
            result = jsonpath.jsonpath(msg.json(), '$..vendorCode')[0]
            assert result == expect
        else:
            result = jsonpath.jsonpath(msg.json(), '$..state')[0]
            assert result == 1

    @pytest.mark.parametrize("key,value,expect", testdata["vendorQualityQuestion_page_data"],
                             ids=["事故单号", "查询工厂编码"])
    @allure.feature('新建质量问题查询')  # 测试报告显示测试功能
    def test_vendorQualityQuestion_page(self, gettokenfixture, key, value, expect):
        s = gettokenfixture
        self.log.info("----新建质量问题查询接口----")
        r = SRMBase(s)
        msg = r.vendorQualityQuestion_page(key, value)
        self.log.info("获取请求结果: %s" % msg.json())
        if key == "qualityTroubleNo":
            result = jsonpath.jsonpath(msg.json(), '$..qualityTroubleNo')[0]
            assert result == expect
        else:
            result = jsonpath.jsonpath(msg.json(), '$..plantCode')[0]
            assert result == "6199"

    @pytest.mark.parametrize("purchasePerson,expect", testdata["vendorQualityQuestion_save_data"],
                             ids=["保存数据采购员为吴茜", "保存数据采购员为钟子鉴"])
    @allure.feature('新增质量问题保存')
    def test_vendorQualityQuestion_save(self, gettokenfixture, purchasePerson, expect):
        s = gettokenfixture
        self.log.info("-----新增质量问题保存-----")
        r = SRMBase(s)
        msg = r.vendorQualityQuestion_save(purchasePerson)
        result = msg[0]
        self.log.info("获取请求结果{}".format(result.json()))
        assert result.json()["success"] == 1
        assert result.status_code == 200

    @pytest.mark.parametrize("key,value,expect", testdata["vendorBankInfoManage_page_data"],
                             ids=["供应商编码对应银行信息", "查询银行状态已完善"])
    @allure.feature('银行信息管理数据查询')  # 测试报告显示测试功能
    def test_vendorBankInfoManage_page(self, gettokenfixture, key, value, expect):
        s = gettokenfixture
        self.log.info("----银行信息管理数据查询接口----")
        r = SRMBase(s)
        msg = r.vendorBankInfoManage_page(key, value)
        self.log.info("获取请求结果: %s" % msg.json())
        if key == "vendorCode":
            result = jsonpath.jsonpath(msg.json(), '$..vendorCode')[0]
            assert result == expect
        else:
            result = jsonpath.jsonpath(msg.json(), '$..bankStatus')[0]
            assert result == 300

    @pytest.mark.parametrize("purchasePerson", testdata["vendorQualityQuestion_add_data"],
                             ids=["新建质量问题提交采购员1", "新建质量问题提交采购员2"])
    @allure.feature('新建质量问题提交')
    def test_vendorQualityQuestion_add(self, gettokenfixture,  purchasePerson):
        s = gettokenfixture
        self.log.info("----新建质量问题提交接口----")
        r = SRMBase(s)
        msg = r.vendorQualityQuestion_add(purchasePerson)
        result = msg[0]
        self.log.info("获取请求结果{}".format(result.json()))
        assert result.json()["success"] == 1
        assert result.status_code == 200