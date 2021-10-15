# -*- coding: utf-8 -*-
"""
@Time: 2021/7/14 16:32
@Author: zzhang zzhang@cenboomh.com
@File: ModelUpdate.py
@desc:
"""
from collect.service_imp.flow.omnis_flow import ServiceOmnisFlowService
from collect.utils.collect_utils import get_safe_data


class ConfigService(ServiceOmnisFlowService):
    cf_const = {
        "flow_name": "config"
    }
    config_app_config = None

    def __init__(self, op_user):
        ServiceOmnisFlowService.__init__(self, op_user)
        if not ConfigService.config_app_config:
            ConfigService.config_app_config = self.get_third_application(self.get_config_flow_name())

        pass

    def get_app_config(self):
        return ConfigService.config_app_config

    def handler_current_node(self, current):
        config = self.get_app_config()
        result = self.handler_app(current, config)
        return result

    def get_config_flow_name(self):
        return self.cf_const["flow_name"]

    def get_config_flow(self):
        return get_safe_data(self.get_config_flow_name(), self.template)

    def execute(self, handler_node):
        self.set_flow(self.get_config_flow())
        self.set_flow_name(self.get_config_flow_name())
        flow_result = self.flow(handler_node)
        return flow_result

    def result(self, params):
        flow = self.get_config_flow()
        if not flow:
            return self.fail(msg="没有找到" + self.get_config_flow_name() + "节点，请检查配置")
        flow_result = self.execute(self.handler_current_node)
        if not self.is_success(flow_result):
            return flow_result
        return self.success({})

    # def result(self, params=None):
    #     config_data = self.get_config_data()
    #     tree = []
    #     count = 0
    #     for key in config_data:
    #         group = {"key": key,
    #                  "iconSkin": "insight-file",
    #                  "children": []}
    #         services = config_data[key]
    #         for child_key in services:
    #             child = services[child_key]
    #             child["iconSkin"] = "insight-service"
    #             group["children"].append(child)
    #             count += 1
    #         tree.append(group)
    #     return self.success(data=tree, count=count)
