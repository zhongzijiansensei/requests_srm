import allure
import requests
import pytest
from common.logger import Log
from common.read_yaml import ReadYaml
from api.SRM_Base import SRMBase
import json
import jsonpath
from common.connect_oracle import Db_Oracle
import os
import uuid


class TestSrmCp:
    log = Log()
    testdata = ReadYaml("case_data.yml").get_yaml_data()

    @pytest.mark.parametrize("key,value,expect", testdata["cpLackMaterialSub_page_data"],
                             ids=["查询采购申请号",
                                  "查询备注"
                                  ])
    @allure.feature('登录测试用例接口')  # 测试报告显示测试功能
    @allure.step('账号，密码登录')
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
    @pytest.mark.parametrize("caigouyuan,remark,expect",testdata["cpLackMaterialSub_save_data"])
    def test_cpLackMaterialSub_save(self, gettokenfixture, caigouyuan, remark, expect):
        s = gettokenfixture
        self.log.info("-----采购申请保存接口-----")
        r = SRMBase(s)
        msg = r.cpLackMaterialSub_save(caigouyuan, remark)
        self.log.info("获取请求结果:%s"%msg.json())
        assert msg.json()["success"] == 1