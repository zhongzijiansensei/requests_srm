import allure
import jsonpath
import pytest

from api.SRM_Base import SRMBase
from common.connect_oracle import Db_Oracle
from common.logger import Log
from common.read_yaml import ReadYaml


@pytest.fixture(scope="function")
def cgsqdelete_sql():
    sql = "UPDATE CP_PURCHASE_REQUEST SET STATE = 1 WHERE PURCHASE_REQUEST_ID ='e0e35c96-f309-42c7-a35c-96f30902c7fd'"
    Db_Oracle().update(sql)


@pytest.fixture(scope="function")
def cgsqclear(gettokenfixture):
    s = gettokenfixture
    r = SRMBase(s)
    r.cpLackMaterialSub_leadin_clear()
    print("清空")
    yield s
    r.cpLackMaterialSub_leadin_clear()
    print("后置清空")


class TestSrmCp:
    log = Log()
    testdata = ReadYaml("case_data.yml").get_yaml_data()


    @pytest.mark.parametrize("key,value,expect", testdata["cpLackMaterialSub_page_data"],
                             ids=["查询采购申请号", "查询备注"])
    @allure.feature('采购申请查询接口')  # 测试报告显示测试功能
    def test_cpLackMaterialSub_page(self, gettokenfixture, key, value, expect):
        s = gettokenfixture
        self.log.info("----采购申请查询接口口----")
        r = SRMBase(s)
        msg = r.cpLackMaterialSub_page(key, value)
        self.log.info("获取请求结果: %s" % msg.json())
        if key == "purchaseRequestNo":
            result = jsonpath.jsonpath(msg.json(), '$..purchaseRequestNo')[0]
            assert result == expect
        else:
            result = jsonpath.jsonpath(msg.json(), '$..remark')[0]
            assert expect in result

    @pytest.mark.parametrize("caigouyuan,expect", testdata["cpLackMaterialSub_save_data"],
                             ids=["修改采购员为杨波保存", "修改采购员为钟子鉴保存"])
    @allure.feature('采购申请保存接口')
    def test_cpLackMaterialSub_save(self, gettokenfixture, caigouyuan, expect):
        s = gettokenfixture
        self.log.info("-----采购申请保存接口-----")
        r = SRMBase(s)
        msg = r.cpLackMaterialSub_save(caigouyuan)
        jg = msg[0]
        self.log.info("获取请求结果:%s" % jg.json())
        rem = r.cpLackMaterialSub_page("purchaseRequestNo", "PR2021032000011")
        print(rem.json())
        rem.cgy = jsonpath.jsonpath(rem.json(), '$..buyerAccount')[0]
        rem.rem = jsonpath.jsonpath(rem.json(), '$..remark')[0]
        assert jg.json()["success"] == 1
        assert rem.cgy == expect
        assert rem.rem == "{}".format(msg[1])

    @pytest.mark.parametrize("code, caigouyuan, expect", testdata["cpLackMaterialSub_push_data"],
                             ids=["zzj提交物料1", "yb提交物料2", "zzj提交物料3"])
    @allure.feature('采购申请提交')
    def test_cpLackMaterialSub_push(self, gettokenfixture, code, caigouyuan, expect):
        s = gettokenfixture
        self.log.info("----采购申请提交接口----")
        r = SRMBase(s)
        uid = r.srm_uuid()
        r.cpLackMaterialSub_Temp(uid, code, demand=1)
        msg = r.cpLackMaterialSub_push(uid, caigouyuan)
        result = msg[0]
        self.log.info("获取请求结果{}".format(result.json()))
        uu = msg[1]
        ass_uu = r.cpLackMaterialSub_page("remark", uu)
        ass_remark = jsonpath.jsonpath(ass_uu.json(), '$..remark')[0]
        assert result.json()["success"] == 1
        assert result.status_code == 200
        assert ass_remark == "{}".format(uu)

    @pytest.mark.parametrize("p_id, expect", testdata["cpLackMaterialSub_delete_data"],
                             ids=["正常删除", "删除已发布的数据", "删除已关闭的数据", "删除已完成的数据"])
    @allure.feature('采购申请删除')
    def test_cpLackMaterialSub_delete(self, gettokenfixture, cgsqdelete_sql, p_id, expect):
        s = gettokenfixture
        self.log.info("---采购申请删除接口---")
        r = SRMBase(s)
        msg = r.cpLackMaterialSub_delete(p_id)
        print(msg.json())
        STATUS_sql = "SELECT STATUS FROM CP_PURCHASE_REQUEST WHERE PURCHASE_REQUEST_ID = '{}'".format(p_id)
        STATE_sql = "SELECT STATE FROM CP_PURCHASE_REQUEST WHERE PURCHASE_REQUEST_ID = '{}'".format(p_id)
        jg = Db_Oracle().select(STATUS_sql)
        jh = Db_Oracle().select(STATE_sql)
        ass_jg = jg['STATUS']
        ass_jh = jh['STATE']
        if ass_jg == 100:
            assert ass_jh == 0
        else:
            assert msg.json()["msg"] == expect

    @pytest.mark.parametrize("file", testdata["cpLackMaterialSub_leadin_data"],
                             ids=["导入正确数据", "导入错误数据"])
    @allure.feature('采购申请导入')
    def test_cpLackMaterialSub_leadin(self, gettokenfixture, file):
        s = gettokenfixture
        self.log.info("---采购申请导入---")
        r = SRMBase(s)
        count = r.cpLackMaterialSub_count("createBy", "zhongzijian")
        ass = count.json()["data"]["total"]
        msg = r.cpLackMaterialSub_leadin(file)
        self.log.info("导入结果是%s" % msg.json())
        r.cpLackMaterialSub_leadin_commit()
        count2 = r.cpLackMaterialSub_count("createBy", "zhongzijian")
        ass2 = count2.json()["data"]["total"]
        if file == "c:/cpLackMaterialSub_leadin.xlsx":
            assert ass2 - 1 == ass
        else:
            assert ass2 == ass

    @pytest.mark.parametrize("c1, expect", testdata["cpLackMaterialSub_leadin_edit_data"],
                             ids=["改成正确数据", "改成错误数据"])
    @allure.feature('采购申请编辑与清空')
    def test_cpLackMaterialSub_leadin_edit(self, cgsqclear, c1, expect):
        s = cgsqclear
        self.log.info("采购申请编辑与清空")
        r = SRMBase(s)
        leadin = r.cpLackMaterialSub_leadin("c:/cpLackMaterialSub_leadin.xlsx")
        self.log.info("导入结果是%s" % leadin.json())
        data = r.cpLackMaterialSub_leadin_page("column12", "自动化导入")
        self.log.info("查询结果是{}".format(data.json()))
        lid = jsonpath.jsonpath(data.json(), '$..id')[0]
        self.log.info("抓取到lid是%s" % lid)
        r.cpLackMaterialSub_leadin_edit(lid, c1)
        msg = r.cpLackMaterialSub_leadin_page("column12", "自动化导入")
        msg_id = jsonpath.jsonpath(msg.json(), '$..column1')[0]
        assert msg_id == expect

    @pytest.mark.prod
    @pytest.mark.parametrize("detailstatus, status, ds_expect, s_expect", testdata["cpdetail_statuspage_data"],
                             ids=["查询待提交", "查询已发布", "查询已关闭", "查询已完成",
                                  "查询未分配", "查询部分分配", "查询部分转单", "查询部分下单",
                                  "查询已分配", "查询已转单", "查询明细完成", "查询明细已关闭"])
    @allure.feature('采购申请明细状态查询')
    def test_cpdetail_statuspage_data(self, gettokenfixture, detailstatus, status, ds_expect, s_expect):
        s = gettokenfixture
        self.log.info("---采购申请明细状态查询---")
        r = SRMBase(s)
        msg = r.cpdetail_statuspage(detailstatus, status)
        ass_ds = jsonpath.jsonpath(msg.json(), '$..requestDetailStatus')[0]
        ass_s = jsonpath.jsonpath(msg.json(), '$..status')[0]
        ass1 = repr(ass_ds)
        ass2 = repr(ass_s)
        assert ass1 in ds_expect
        assert ass2 in s_expect

    @pytest.mark.parametrize("key,value,expect", testdata["cpdetail_page_data"],
                             ids=["查询采购申请号", "查询物料", "查询采购员"])
    @allure.feature('采购申请明细查询接口口')
    def test_cpdetail_page(self, gettokenfixture, key, value, expect):
        s = gettokenfixture
        self.log.info("----采购申请明细查询接口口----")
        r = SRMBase(s)
        msg = r.cpdetail_page(key, value)
        self.log.info("获取请求结果: %s" % msg.json())
        if key == "purchaseRequestNo":
            result = jsonpath.jsonpath(msg.json(), '$..purchaseRequestNo')[0]
            assert result == expect
        elif key == "materialCode":
            result = jsonpath.jsonpath(msg.json(), '$..materialCode')[0]
            assert result == expect
        else:
            result = jsonpath.jsonpath(msg.json(), '$..buyerAccount')[0]
            assert result == expect

    @pytest.mark.parametrize("value,expect", testdata["cpdetail_userpage_data"],
                             ids=["查询采购员wx", "查询采购员zzj"])
    @allure.feature('转交采购员查询接口')
    def test_cpdetail_userpage(self, gettokenfixture, value, expect):
        s = gettokenfixture
        self.log.info("---转交采购员查询接口---")
        r = SRMBase(s)
        msg = r.cpdetail_userpage(value)
        self.log.info("获取请求结果:%s" % msg.json())
        assert msg.json()["msg"] == expect["msg"]

    @pytest.mark.parametrize("account", testdata["cpdetail_transfer_data"],
                             ids=["转交采购员wx", "转交采购员zzj"])
    @allure.feature('采购申请明细转交接口')
    def test_cpdetail_transfer(self, gettokenfixture, account):
        s = gettokenfixture
        self.log.info("---采购申请明细转交接口---")
        r = SRMBase(s)
        r.cpdetail_transfer(account)
        msg = r.cpdetail_page("purchaseRequestNo", "PR2021042000011")
        self.log.info("转交后查询结果:%s" % msg.json())
        ass = jsonpath.jsonpath(msg.json(), '$..buyerAccount')[0]
        assert ass == account

    @allure.feature('采购申请明细导出接口')
    def test_cpdetail_report(self, gettokenfixture):
        s = gettokenfixture
        r = SRMBase(s)
        self.log.info("---采购申请明细导出---")
        msg = r.cpdetail_report()
        assert msg.status_code == 200

    @allure.feature('采购申请查看-获取供应商接口')
    def test_cpselect_vendor(self, gettokenfixture):
        s = gettokenfixture
        self.log.info('---采购申请查看-获取供应商接口---')
        r = SRMBase(s)
        msg = r.cpselect_vendor()
        assert msg.status_code == 200

    @allure.feature('采购申请查看-获取公司接口')
    def test_cpselect_baseCompany(self, gettokenfixture):
        s = gettokenfixture
        self.log.info('---采购申请查看-获取公司接口---')
        r = SRMBase(s)
        msg = r.cpselect_baseCompany()
        assert msg.status_code == 200

    @allure.feature("采购申请查看-获取采购员接口")
    def test_cpselect_sysUser(self, gettokenfixture):
        s = gettokenfixture
        self.log.info('---采购申请查看-获取采购员接口---')
        r = SRMBase(s)
        msg = r.cpselect_sysUser()
        assert msg.json()["msg"] == "获取用户成功"

    @allure.feature("采购申请查看-获取主单接口")
    def test_cpselect_main(self, gettokenfixture):
        s = gettokenfixture
        self.log.info('---采购申请查看-获取主单接口---')
        r = SRMBase(s)
        msg = r.cpselect_main()
        self.log.info('获取结果是:%s' % msg.json())
        assert msg.json()["data"]["tempId"] == "8e926428-c823-418d-9264-28c823a18d03"

    @allure.feature("采购申请查看-获取明细接口")
    def test_cpselect_temp(self, gettokenfixture):
        s = gettokenfixture
        self.log.info("---采购申请查看-获取明细接口---")
        r = SRMBase(s)
        msg = r.cpselect_temp()
        self.log.info('获取结果是:%s' % msg.json())
        a_msg = jsonpath.jsonpath(msg.json(), '$..tempId')[0]
        assert a_msg == "8e926428-c823-418d-9264-28c823a18d03"

    @allure.feature("采购申请查看-获取日志接口")
    def test_cpselect_log(self, gettokenfixture):
        s = gettokenfixture
        self.log.info("---采购申请查看-获取日志接口---")
        r = SRMBase(s)
        msg = r.cpselect_log()
        self.log.info("获取结果是:%s" % msg.json())
        a_msg = jsonpath.jsonpath(msg.json(), '$..busId')[0]
        assert a_msg == "8e926428-c823-418d-9264-28c823a18d03"

    @pytest.mark.parametrize("syncstatus, status, ss_expect, s_expect", testdata["cp_statuspage_data"],
                             ids=["查询待提交", "查询已发布", "查询已关闭", "查询已完成",
                                  "查询未同步", "查询同步中", "查询同步失败", "查询同步成功", "查询不同步"])
    @allure.feature("采购申请状态查询接口")
    def test_cp_statuspage(self, gettokenfixture, syncstatus, status, ss_expect, s_expect):
        s = gettokenfixture
        self.log.info("采购申请状态查询接口")
        r = SRMBase(s)
        msg = r.cp_statuspage(syncstatus, status)
        self.log.info("获取结果是:%s" % msg.json())
        ass_ss = jsonpath.jsonpath(msg.json(), '$..syncStatus')[0]
        ass_s = jsonpath.jsonpath(msg.json(), '$..status')[0]
        ass1 = repr(ass_ss)
        ass2 = repr(ass_s)
        assert ass1 in ss_expect
        assert ass2 in s_expect

    @pytest.mark.parametrize("status, expect", testdata["cp_examineRecordsPage_data"],
                             ids=["查询待审核", "查询审核未通过", "查询已通过"])
    @allure.feature("配额超标审核记录状态查询")
    def test_cp_examineRecordsPage(self, gettokenfixture, status, expect):
        s = gettokenfixture
        self.log.info("配额超标审核记录状态查询")
        r = SRMBase(s)
        msg = r.cp_examineRecordsPage(status)
        self.log.info("获取的结果是:%s" % msg.json())
        a_msg = jsonpath.jsonpath(msg.json(), '$..status')[0]
        assert a_msg == expect

    @pytest.mark.parametrize("key, value", testdata["cp_examineRecordsPg_data"],
                             ids=["查询采购申请单号", "查询物料编码"])
    @allure.feature("配额超标审核记录查询")
    def test_cp_examineRecordsPg(self, gettokenfixture, key, value):
        s = gettokenfixture
        self.log.info("配额超标审核记录查询")
        r = SRMBase(s)
        msg = r.cp_examineRecordsPg(key, value)
        self.log.info("获取的结果是:%s" % msg.json())
        a_msg = jsonpath.jsonpath(msg.json(), '$..purchaseRequestNo')[0]
        b_msg = jsonpath.jsonpath(msg.json(), '$..materialCode')[0]
        if key == "purchaseRequestNo":
            assert a_msg == value
        else:
            assert b_msg == value

    @pytest.mark.parametrize("key, status, expect", testdata["cp_zdstatusPage_data"],
                             ids=["查询未分配", "查询部分分配", "查询部分转单", "查询部分下单", "查询已分配",
                                  "查询已转单", "查询已完成", "查询已关闭"])
    @allure.feature("采购申请转单状态查询")
    def test_cp_zdstatusPage(self, gettokenfixture, key, status, expect):
        s = gettokenfixture
        self.log.info("采购申请转单状态查询")
        r = SRMBase(s)
        msg = r.cp_zdstatusPage(key, status)
        self.log.info("获取的结果是:%s" % msg.json())
        a_msg = jsonpath.jsonpath(msg.json(), '$..requestDetailStatus')[0]
        assert a_msg == expect

    @pytest.mark.parametrize("key, value, expect", testdata["cp_zdpage_data"],
                             ids=["查询备注", "查询创建人"])
    @allure.feature("采购申请转单查询")
    def test_cp_zdpage(self, gettokenfixture, key, value, expect):
        s = gettokenfixture
        self.log.info("采购申请转单查询")
        r = SRMBase(s)
        msg = r.cp_zdpage(key, value)
        self.log.info("获取请求结果:%s" % msg.json())
        a_msg = jsonpath.jsonpath(msg.json(), '$..requestDetailRemark')[0]
        b_msg = jsonpath.jsonpath(msg.json(), '$..createBy')[0]
        if key == "requestDetailRemark":
            assert a_msg == expect
        else:
            assert b_msg == expect

    @allure.feature("采购申请明细分配查询")
    def test_cp_zdqueryAllpage(self, gettokenfixture):
        s = gettokenfixture
        self.log.info("采购申请明细分配查询")
        r = SRMBase(s)
        msg = r.cp_zdqueryAllpage()
        self.log.info("获取结果是:%s" % msg.json())
        assert "allotQty" in msg.text

    @pytest.mark.parametrize("bool, expect", testdata["cp_cpzdcommit_data"],
                             ids=["采购申请转单提交","采购申请转单保存"])
    @allure.feature("采购申请转单提交与保存")
    def test_cpzdcommit(self, gettokenfixture, bool, expect):
        s = gettokenfixture
        self.log.info("---采购申请转单提交---")
        r = SRMBase(s)
        try:
            msg_getRequestid = r.cp_zdpage("requestDetailRemark", "自动化导入")  # 查询目标采购申请
            Requestid = jsonpath.jsonpath(msg_getRequestid.json(), '$..purchaseRequestId')[0]
            Detailid = jsonpath.jsonpath(msg_getRequestid.json(), '$..requestDetailId')[0]
            self.log.info("获取采购申请ID:%s" % Requestid)
        except:
            self.log.error("自动化导入数据已耗尽")
        msg_allotDty = r.cp_zdallotDty(Requestid, Detailid)  # 分配采购申请
        Alloid = msg_allotDty.json()["data"][0]
        self.log.info("分配的ID是:%s" % msg_allotDty.json()["data"][0])
        msg_commit = r.cp_zdcommit(Requestid, Detailid, Alloid)  # 分配页面的提交
        self.log.info("提交的结果是:%s" % msg_commit.json())
        msg_traceid = r.cp_queryByCompanyVendor("500973", "6100", "A01")  # 获取可提交明细
        for jg in msg_traceid.json()['data']:
            if jg['requestAllotId'] == Alloid:
                break
        Tranceid = jg['requestTransferId']
        msg_jlcommit = r.cp_zdjlcommit(Tranceid, Detailid, Alloid)  # 转单页面的提交
        tempid = msg_jlcommit.json()["data"]["tempId"]
        self.log.info("获取的tempID是:%s" % tempid)
        msg_page = r.cp_ordertempPage(tempid)  # 根据tempid查询获取传参
        detailtempid = jsonpath.jsonpath(msg_page.json(), '$..detailTempId')[0]
        orderdetailid = jsonpath.jsonpath(msg_page.json(), '$..orderDetailId')[0]
        msg_put = r.cp_orderDetailEdit(tempid, detailtempid, Tranceid, orderdetailid)  #更新采购订单明细
        try:
            msg_jccommit = r.cp_cgsqjccommit(tempid, bool)  # 最后提交采购订单
            self.log.info("生成采购订单号是:%s" % msg_jccommit.json()["msg"])
        except:
            self.log.error("采购订单提交失败")
        msg = r.cp_orderpage("purchaseOrderNo", msg_jccommit.json()["msg"])
        status = jsonpath.jsonpath(msg.json(), '$..status')[0]
        assert msg.json()["data"]["total"] == 1
        assert status == expect

    @allure.feature("采购申请转单取消分配")
    def test_cpzdcancel(self, gettokenfixture):
        s = gettokenfixture
        self.log.info("采购申请转单取消分配")
        r = SRMBase(s)
        RequestsNo = r.cp_zdstatusPage("requestDetailStatus100", "100")
        print("请求结果是%s"%RequestsNo.text)
        No = jsonpath.jsonpath(RequestsNo.json(), '$..purchaseRequestNo')[0]
        Requestid = jsonpath.jsonpath(RequestsNo.json(), '$..purchaseRequestId')[0]
        Detailid = jsonpath.jsonpath(RequestsNo.json(), '$..requestDetailId')[0]
        Dty = r.cp_zdallotDty(Requestid, Detailid)
        Alloid = Dty.json()["data"][0]
        msg = r.cp_zdcacle(Alloid, Requestid, Detailid, No)
        self.log.info("取消结果是:%s" % msg.text)
        ass_No = r.cp_zdpage("purchaseRequestNo", No)
        assert ass_No.json()["data"]["total"] == 1

    @allure.feature("采购申请转单取消")
    def test_cpPurchase_cancel(self, gettokenfixture):
        s = gettokenfixture
        self.log.info("采购申请转单取消")
        r = SRMBase(s)
        data = r.cp_queryByCompanyVendor("500973", "6100", "A01")
        print(data.json())
        for i in data.json()['data']:
            if i['purchaseRequestNo'] == "purchaseRequestNo":
                break
        TransferId = i["requestTransferId"]
        batchFlag = i["batchFlag"]
        cancel = r.cpPurchase_cancel(batchFlag, TransferId)
        self.log.info("取消返回结果:%s" % cancel.text)
        msg = r.cp_zdqueryAllpage()
        reset = r.cp_zdcommit("8e926428-c823-418d-9264-28c823a18d03", "448ad576-bcc5-4689-8ad5-76bcc5d68971",
                              "8ce3691f-136f-49c6-a369-1f136ff9c6a0")
        for j in msg.json()['data']:
            if j['purchaseRequestNo'] == "PR2021042100008":
                break
        assert j["purchaseRequestNo"] == "PR2021042100008"

    @pytest.mark.parametrize("auditFlag, expect", testdata["cp_audit_data"],
                             ids=["审核通过", "审核驳回"])
    @allure.feature("配额超标审核")
    def test_cpPurchaseRequestOverproof(self, gettokenfixture, auditFlag, expect):
        s = gettokenfixture
        self.log.info("----采购申请配额超标审核----")
        r = SRMBase(s)
        uid = r.srm_uuid()
        r.cpLackMaterialSub_Temp(uid, code="105000007", demand=401)  # 超标采购申请新增
        msg = r.cpLackMaterialSub_push(uid, caigouyuan="zhongzijian")
        result = msg[0]
        self.log.info("获取新增结果{}".format(result.json()))
        try:
            msg_getRequestid = r.cp_zdpage(key="materialCode", value="105000007")  # 查询目标采购申请
            Requestid = jsonpath.jsonpath(msg_getRequestid.json(), '$..purchaseRequestId')[0]
            Detailid = jsonpath.jsonpath(msg_getRequestid.json(), '$..requestDetailId')[0]
            self.log.info("获取采购申请ID:%s" % Requestid)
        except:
            self.log.error("获取采购申请数据错误")
        msg_allotDty = r.cp_zdallotDty(Requestid, Detailid)  # 分配采购申请
        Alloid = msg_allotDty.json()["data"][0]
        commit = r.cp_zdcomits(Requestid, Detailid, Alloid)  #分配页面提交
        sql = "UPDATE BUSINESS_WAIT_APPROVE_RECORD SET APPROVE_BY = 'zhongzijian' WHERE PROCESS_NAME = '采购申请超标审批流'"
        Db_Oracle().update(sql)
        page = r.cp_customPage("materialCode", "105000007")
        auditid = jsonpath.jsonpath(page.json(), '$..requestOverproofId')[0]
        purchaseRequestNo = jsonpath.jsonpath(page.json(), '$..purchaseRequestNo')[0]
        msg = r.cp_audit(auditid, auditFlag)
        self.log.info("审核结果是:%s"%msg.json())
        ass = r.cp_examineRecordsPg("purchaseRequestNo", purchaseRequestNo)
        status = jsonpath.jsonpath(ass.json(), '$..status')[0]
        assert status == expect

    @pytest.mark.parametrize("key, value", testdata["cp_customPage_data"],
                             ids=["查询单号", "查询物料"])
    @allure.feature("配额超标审核查询")
    def test_customPage(self, gettokenfixture, key, value):
        s = gettokenfixture
        self.log.info("配额超标审核查询")
        r = SRMBase(s)
        msg = r.cp_customPage(key, value)
        self.log.info("查询结果为:%s" % msg.json())
        purchaseRequestNo = jsonpath.jsonpath(msg.json(), '$..purchaseRequestNo')[0]
        materialCode = jsonpath.jsonpath(msg.json(), '$..materialCode')[0]
        if key == "materialCode":
            assert materialCode == value
        else:
            assert purchaseRequestNo == value

    @pytest.mark.parametrize("key, value", testdata["cpLackMaterialSub_statusPage_Data"],
                             ids=["查询待提交", "查询采购员待确认", "查询库房待收货",
                                  "查询库房收货中", "查询完成"])
    @pytest.mark.prod
    @allure.feature("缺料提报状态查询")
    def test_cpLackMaterialSub_statusPage(self, gettokenfixture, key, value):
        s = gettokenfixture
        self.log.info("缺料提报状态查询接口")
        r = SRMBase(s)
        msg = r.cpLackMaterialSub_statusPage(key, value)
        status = jsonpath.jsonpath(msg.json(), '$..status')[0]
        self.log.info("查询结果是:%s" %msg.json())
        assert status == value

    @pytest.mark.parametrize("key, value", testdata["cpLackMaterialSub_qlpage_Data"],
                             ids=["查询缺料提报编码", "查询物料", "查询提报人"])
    @pytest.mark.prod
    @allure.feature("缺料提报查询")
    def test_cpLackMaterialSub_statusPage(self, gettokenfixture, key, value):
        s = gettokenfixture
        self.log.info("缺料提报查询接口")
        r = SRMBase(s)
        msg = r.cpLackMaterialSub_qlpage(key, value)
        lackMaterialSubNo = jsonpath.jsonpath(msg.json(), '$..lackMaterialSubNo')[0]
        materialCode = jsonpath.jsonpath(msg.json(), '$..materialCode')[0]
        createBy = jsonpath.jsonpath(msg.json(), '$..createBy')[0]
        self.log.info("查询结果是:%s" % msg.json())
        if key == "lackMaterialSubNo":
            assert lackMaterialSubNo == value
        elif key == "materialCode":
            assert materialCode == value
        else:
            assert createBy == value

    @allure.feature("根据公司查询工厂")
    def test_basePlant(self, gettokenfixture):
        s = gettokenfixture
        self.log.info("根据公司查询工厂")
        r = SRMBase(s)
        msg = r.basePlant()
        self.log.info("查询第一条结果是:%s"%msg.json()["data"][0])
        assert msg.json()["msg"] == "查询成功"

    @allure.feature("根据工厂查询库位")
    def test_baseStorageLocation(self, gettokenfixture):
        s = gettokenfixture
        self.log.info("根据工厂查询库位")
        r = SRMBase(s)
        msg = r.baseStorageLocation()
        self.log.info("查询第一条结果是:%s"%msg.json()["data"][0])
        assert msg.json()["msg"] == "查询成功"

    @allure.feature("根据工厂获取物料")
    def test_customByPlantPage(self, gettokenfixture):
        s = gettokenfixture
        self.log.info("根据工厂获取物料")
        r = SRMBase(s)
        msg = r.customByPlantPage()
        self.log.info("查询到第一页条数是:%s" %msg.json()["data"]["total"])
        assert msg.json()["success"] == 1
        assert msg.json()["data"]["total"] == 6

    @pytest.mark.parametrize("processamento", testdata["cpLackMaterialSub_add_data"],
                             ids=["新增质量不合格缺料提报",
                                  "新增有货不可用缺料提报",
                                  "新增采购缺料提报"])
    @allure.feature("缺料提报新增")
    def test_cpLackMaterialSub_add(self, gettokenfixture, processamento):
        s = gettokenfixture
        self.log.info("缺料提报新增")
        r = SRMBase(s)
        msg = r.cpLackMaterialSub_add(processamento)
        ass = r.cpLackMaterialSub_qlpage("productName", msg[1])
        ass_processamento = jsonpath.jsonpath(ass.json(), '$..processamento')[0]
        assert ass_processamento == processamento

    @pytest.mark.parametrize("processamento", testdata["cpLackMaterialSub_Save_Data"],
                             ids=["新增质量不合格缺料提报保存",
                                  "新增有货不可用缺料提报保存",
                                  "新增采购缺料提报保存"])
    @allure.feature("缺料提报保存")
    def test_cpLackMaterialSub_Save(self, gettokenfixture, processamento):
        s = gettokenfixture
        self.log.info("缺料提报保存")
        r = SRMBase(s)
        msg = r.cpLackMaterialSub_Save(processamento)
        ass = r.cpLackMaterialSub_qlpage("productName", msg[1])
        ass_processamento = jsonpath.jsonpath(ass.json(), '$..processamento')[0]
        ass_status = jsonpath.jsonpath(ass.json(), '$..status')[0]
        assert ass_processamento == processamento
        assert ass_status == 100

    @pytest.mark.parametrize("processamento", testdata["cpLackMaterialSub_EditSave_Data"],
                             ids=["编辑质量不合格缺料提报保存",
                                  "编辑有货不可用缺料提报保存",
                                  "编辑采购缺料提报保存"])
    @allure.feature("缺料提报编辑保存")
    def test_cpLackMaterialSub_EditSave(self, gettokenfixture, processamento):
        s = gettokenfixture
        self.log.info("缺料提报编辑保存")
        r = SRMBase(s)
        msg = r.cpLackMaterialSub_EditSave(processamento)
        page = r.cpLackMaterialSub_qlpage("productName","3e316193-33d7-4dbe-b161" )
        ass_processamento = jsonpath.jsonpath(page.json(), '$..processamento')[0]
        assert msg.json()["success"] == 1
        assert ass_processamento == processamento

    @pytest.mark.parametrize("processamento", testdata["cpLackMaterialSub_EditSave_Data"],
                             ids=["编辑质量不合格缺料提报提交",
                                  "编辑有货不可用缺料提报提交",
                                  "编辑采购缺料提报提交"])
    @allure.feature("缺料提报编辑保存")
    def test_cpLackMaterialSub_EditSave(self, gettokenfixture, processamento):
        s = gettokenfixture
        self.log.info("缺料提报编辑保存")
        r = SRMBase(s)
        msg = r.cpLackMaterialSub_EditSave(processamento)
        page = r.cpLackMaterialSub_qlpage("productName", "3e316193-33d7-4dbe-b161")
        ass_processamento = jsonpath.jsonpath(page.json(), '$..processamento')[0]
        assert msg.json()["success"] == 1
        assert ass_processamento == processamento

    @pytest.mark.parametrize("key, value", testdata["lackMaterial_data"],
                             ids=["删除待提交数据","删除待确认数据"])
    @allure.feature("缺料提报删除")
    def test_lackMaterial(self, gettokenfixture, key, value):
        s = gettokenfixture
        self.log.info("缺料提报删除")
        r = SRMBase(s)
        page = r.cpLackMaterialSub_statusPage(key, value)
        self.log.info("查询第一条是:%s" % page.json()["data"]["records"][0])
        lackMaterialSubId = jsonpath.jsonpath(page.json(), '$..lackMaterialSubId')[0]
        msg = r.lackMaterial(lackMaterialSubId)
        sql = "SELECT STATE FROM CP_LACK_MATERIAL_SUB " \
              "WHERE LACK_MATERIAL_SUB_ID = '%s'" % lackMaterialSubId
        state = Db_Oracle().select(sql)
        assert state["STATE"] == 0

