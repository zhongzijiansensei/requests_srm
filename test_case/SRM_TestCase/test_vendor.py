# -*- coding: UTF-8 -*-

import allure
import pytest
from common.logger import Log
from common.read_yaml import ReadYaml
from api.srm_vendor import Srmvendor
import jsonpath


# from common.connect_oracle import Db_Oracle


@allure.feature("供应商模块测试")
class TestSrmVendor:
    log = Log()
    testdata = ReadYaml("vendor_data.yml").get_yaml_data()

    @pytest.mark.prod
    @pytest.mark.parametrize("key,value,expect", testdata["vendorMasterData_page_data"],
                             ids=["供应商编码", "数据状态"])
    @allure.feature('供应商主数据查询')  # 测试报告显示测试功能
    def test_vendorMasterData_page(self, gettokenfixture, key, value, expect):
        s = gettokenfixture
        self.log.info("----供应商主数据查询接口----")
        r = Srmvendor(s)
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
        r = Srmvendor(s)
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
        r = Srmvendor(s)
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
        r = Srmvendor(s)
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
    def test_vendorQualityQuestion_add(self, gettokenfixture, purchasePerson):
        s = gettokenfixture
        self.log.info("----新建质量问题提交接口----")
        r = Srmvendor(s)
        msg = r.vendorQualityQuestion_add(purchasePerson)
        result = msg[0]
        self.log.info("获取请求结果{}".format(result.json()))
        assert result.json()["success"] == 1
        assert result.status_code == 200

    @pytest.mark.parametrize("source, status, s1_expect, s2_expect", testdata["vendorImport_data"],
                             ids=["供应商引入查询自主注册", "供应商引入查询引入新增", "供应商引入查询潜在重新申请",
                                  "供应商引入查询数据迁移", "供应商引入查询待提交", "供应商引入查询开发员已退回",
                                  "供应商引入查询开发员待确认", "供应商引入查询采购领导退回",
                                  "供应商引入查询开发人员待提交", "供应商引入查询采购领导待审核",
                                  "供应商引入查询未通过", "供应商引入查询已建档"])
    @allure.feature("供应商引入查询接口")
    def test_vendorImport(self, gettokenfixture, source, status, s1_expect, s2_expect):
        s = gettokenfixture
        self.log.info("供应商引入状态查询接口")
        r = Srmvendor(s)
        msg = r.vendorImport(source, status)
        self.log.info("获取结果是:%s"%msg.json())
        ass_s1 = jsonpath.jsonpath(msg.json(), '$..source')[0]
        ass_s2 = jsonpath.jsonpath(msg.json(), '$..status')[0]
        ass1 = repr(ass_s1)
        ass2 = repr(ass_s2)
        assert ass1 in s1_expect
        assert ass2 in s2_expect

    @pytest.mark.parametrize("state, expect", testdata["vendorMasterData_master_page"],
                             ids=["查询供应商主数据数据状态正常", "查询供应商主数据数据状态冻结"])
    @allure.feature("供应商主数据数据状态查询")
    def test_vendorMasterData_master_page(self, gettokenfixture, state, expect):
        s = gettokenfixture
        self.log.info("供应商主数据数据状态查询")
        r = Srmvendor(s)
        msg = r.vendorMasterData_master_page(state)
        self.log.info("获取的结果是:%s" % msg.json())
        a_msg = jsonpath.jsonpath(msg.json(), '$..state')[0]
        assert a_msg == expect

    @pytest.mark.parametrize("status, expect", testdata["vendorChangeInfo_page"],
                             ids=["供应商信息变更管理查询待提交", "供应商信息变更管理查询已退回",
                                  "供应商信息变更管理查询待审核", "供应商信息变更管理查询开发员待确认",
                                  "供应商信息变更管理查询完成"])
    @allure.feature("供应商信息变更管理状态")
    def test_vendorChangeInfo_page(self, gettokenfixture, status, expect):
        s = gettokenfixture
        self.log.info("查询供应商信息变更管理状态")
        r = Srmvendor(s)
        msg = r.vendorChangeInfo_page(status)
        self.log.info("获取的结果是:%s" % msg.json())
        a_msg = jsonpath.jsonpath(msg.json(), '$..status')[0]
        assert a_msg == expect

    @allure.feature('供应商主数据导出接口')
    def test_vendorMasterData_reportExcel(self, gettokenfixture):
        s = gettokenfixture
        r = Srmvendor(s)
        self.log.info("---供应商主数据导出---")
        msg = r.vendorMasterData_reportExcel()
        assert msg.status_code == 200

    @allure.feature('银行信息管理导出接口')
    def test_vendorBankInfoManage_exportExcle(self, gettokenfixture):
        s = gettokenfixture
        r = Srmvendor(s)
        self.log.info("---银行信息管理导出---")
        msg = r.vendorBankInfoManage_exportExcle()
        assert msg.status_code == 200

    @allure.feature('质量问题管理导出数据接口')
    def test_vendorQualityQuestion_export(self, gettokenfixture):
        s = gettokenfixture
        r = Srmvendor(s)
        self.log.info("---质量问题管理数据导出---")
        msg = r.vendorQualityQuestion_export()
        assert msg.status_code == 200

    @pytest.mark.parametrize("bankStatus, expect", testdata["vendorBankInfoManage_page1"],
                             ids=["银行信息待完善", "银行信息待提交",
                                  "银行信息已退回", "银行信息待审核",
                                  "银行信息已完善"])
    @allure.feature("银行信息管理状态")
    def test_vendorBankInfoManage_page1(self, gettokenfixture, bankStatus, expect):
        s = gettokenfixture
        self.log.info("查询银行信息管理状态")
        r = Srmvendor(s)
        msg = r.vendorBankInfoManage_page1(bankStatus)
        self.log.info("获取的结果是:%s" % msg.json())
        a_msg = jsonpath.jsonpath(msg.json(), '$..bankStatus')[0]
        assert a_msg == expect

    @pytest.mark.parametrize("state, status, s1_expect, s2_expect", testdata["vendorBankInfoManage_detail_page"],
                             ids=["供应商银行明细信息查询数据状态正常", "供应商银行明细信息查询数据状态冻结",
                                  "供应商银行明细信息查询审核状态待完善", "供应商银行明细信息查询审核状态待提交",
                                  "供应商银行明细信息查询审核状态已退回", "供应商银行明细信息查询审核状态待审核",
                                  "供应商银行明细信息查询审核状态已完善"])
    @allure.feature("供应商银行明细信息状态查询接口")
    def test_vendorBankInfoManage_detail_page(self, gettokenfixture, state, status, s1_expect, s2_expect):
        s = gettokenfixture
        self.log.info("供应商银行明细信息状态查询")
        r = Srmvendor(s)
        msg = r.vendorBankInfoManage_detail_page(state, status)
        self.log.info("获取结果是:%s" % msg.json())
        ass_s1 = jsonpath.jsonpath(msg.json(), '$..state')[0]
        ass_s2 = jsonpath.jsonpath(msg.json(), '$..status')[0]
        ass1 = repr(ass_s1)
        ass2 = repr(ass_s2)
        assert ass1 in s1_expect
        assert ass2 in s2_expect

    @pytest.mark.parametrize("troubleType, status, t_expect, s_expect", testdata["vendorQualityQuestion_page1"],
                             ids=["新建质量问题查询质量事故", "新建质量问题查询生产事故",
                                  "新建质量问题查询品管-待提交", "新建质量问题查询已退回",
                                  "新建质量问题查询待审核"])
    @allure.feature("新建质量问题事故类型和状态查询接口")
    def test_vendorQualityQuestion_page1(self, gettokenfixture, troubleType, status, t_expect, s_expect):
        s = gettokenfixture
        self.log.info("新建质量问题事故类型和状态查询")
        r = Srmvendor(s)
        msg = r.vendorQualityQuestion_page1(troubleType, status)
        self.log.info("获取结果是:%s" % msg.json())
        ass_t = jsonpath.jsonpath(msg.json(), '$..troubleType')[0]
        ass_s = jsonpath.jsonpath(msg.json(), '$..status')[0]
        ass1 = repr(ass_t)
        ass2 = repr(ass_s)
        assert ass1 in t_expect
        assert ass2 in s_expect

    @pytest.mark.parametrize("troubleType, status, t_expect, s_expect", testdata["vendorQualityQuestion_page2"],
                             ids=["质量问题管理查询质量事故", "质量问题管理查询生产事故",
                                  "质量问题管理查询品管-待提交", "质量问题管理查询待处理",
                                  "质量问题管理查询已退回", "质量问题管理查询待审核",
                                  "质量问题管理查询审核退回", "质量问题管理查询待确认",
                                  "质量问题管理查询待协商", "质量问题管理查询已完成"])
    @allure.feature("质量问题管理事故类型和状态查询接口")
    def test_vendorQualityQuestion_page2(self, gettokenfixture, troubleType, status, t_expect, s_expect):
        s = gettokenfixture
        self.log.info("质量问题管理事故类型和状态查询")
        r = Srmvendor(s)
        msg = r.vendorQualityQuestion_page2(troubleType, status)
        self.log.info("获取结果是:%s" % msg.json())
        ass_t = jsonpath.jsonpath(msg.json(), '$..troubleType')[0]
        ass_s = jsonpath.jsonpath(msg.json(), '$..status')[0]
        ass1 = repr(ass_t)
        ass2 = repr(ass_s)
        assert ass1 in t_expect
        assert ass2 in s_expect