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

    @pytest.mark.prod
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
        r.cpLackMaterialSub_Temp(uid, code)
        msg = r.cpLackMaterialSub_push(uid, caigouyuan)
        result = msg[0]
        self.log.info("获取请求结果{}".format(result.json()))
        uu = msg[1]
        ass_uu = r.cpLackMaterialSub_page("remark", uu)
        ass_remark = jsonpath.jsonpath(ass_uu.json(), '$..remark')[0]
        assert result.json()["success"] == 1
        assert result.status_code == 200
        assert ass_remark == "{}".format(uu)

    @pytest.mark.parametrize("id, expect", testdata["cpLackMaterialSub_delete_data"],
                             ids=["正常删除", "删除已发布的数据", "删除已关闭的数据", "删除已完成的数据"])
    @allure.feature('采购申请删除')
    def test_cpLackMaterialSub_delete(self,gettokenfixture, cgsqdelete_sql,  id, expect):
        s = gettokenfixture
        self.log.info("---采购申请删除接口---")
        r = SRMBase(s)
        msg = r.cpLackMaterialSub_delete(id)
        print(msg.json())
        STATUS_sql = "SELECT STATUS FROM CP_PURCHASE_REQUEST WHERE PURCHASE_REQUEST_ID = '{}'".format(id)
        STATE_sql = "SELECT STATE FROM CP_PURCHASE_REQUEST WHERE PURCHASE_REQUEST_ID = '{}'".format(id)
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
    @allure.feature('采购申请查询接口')
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
                             ids=["查询采购员wx","查询采购员zzj"])
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
    def test_cpselect_baseCompany(self,gettokenfixture):
        s = gettokenfixture
        self.log.info('---采购申请查看-获取公司接口---')
        r = SRMBase(s)
        msg = r.cpselect_baseCompany()
        assert  msg.status_code == 200
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
        self.log.info('获取结果是:%s'% msg.json())
        assert msg.json()["data"]["tempId"] == "8e926428-c823-418d-9264-28c823a18d03"
    @allure.feature("采购申请查看-获取明细接口")
    def test_cpselect_temp(self, gettokenfixture):
        s= gettokenfixture
        self.log.info("---采购申请查看-获取明细接口---")
        r = SRMBase(s)
        msg = r.cpselect_temp()
        self.log.info('获取结果是:%s'% msg.json())
        a_msg = jsonpath.jsonpath(msg.json(), '$..tempId')[0]
        assert a_msg == "8e926428-c823-418d-9264-28c823a18d03"
    @allure.feature("采购申请查看-获取日志接口")
    def test_cpselect_log(self, gettokenfixture):
        s = gettokenfixture
        self.log.info("---采购申请查看-获取日志接口---")
        r = SRMBase(s)
        msg = r.cpselect_log()
        self.log.info("获取结果是:%s"%msg.json())
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
        self.log.info("获取结果是:%s"%msg.json())
        ass_ss = jsonpath.jsonpath(msg.json(), '$..syncStatus')[0]
        ass_s = jsonpath.jsonpath(msg.json(), '$..status')[0]
        ass1 = repr(ass_ss)
        ass2 = repr(ass_s)
        assert ass1 in ss_expect
        assert ass2 in s_expect