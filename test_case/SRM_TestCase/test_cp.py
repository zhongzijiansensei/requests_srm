import allure
import requests
import pytest
from common.logger import Log
from common.read_yaml import ReadYaml
from api.SRM_Base import SRMBase
import jsonpath
from common.connect_oracle import Db_Oracle
import re


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
