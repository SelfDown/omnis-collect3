# -*- coding: utf-8 -*-
"""
@Time: 2021/8/2 16:52
@Author: zzhang zzhang@cenboomh.com
@File: omnis_monitor.py
@desc:
"""
from collect.service_imp.flow.omnis_flow import ServiceOmnisFlowService
from collect.utils.collect_utils import get_safe_data, get_key


class ServiceFlowService(ServiceOmnisFlowService):
    sf_const = {
        "flow_name": "flow",
    }

    def get_flow_name(self):
        return self.sf_const["flow_name"]

    def get_flow(self):
        return get_safe_data(self.get_flow_name(), self.template)

    def handler_current_node(self, current):
        params_result = self.get_params_result()

        # service = get_safe_data(self.get_service_name(), current)
        from collect.service_imp.common.filters.template_tool import TemplateTool
        template_tool = TemplateTool(op_user=self.op_user)
        service = self.get_node_service(current, params_result, template_tool)
        if not self.is_success(service):
            return service
        service = self.get_data(service)
        service_result = self.get_service_result(service, self.template)
        if not self.is_success(service_result):
            return service_result
        data = self.get_data(service_result)
        return self.success(data)

    def execute(self, handler_node):
        self.set_flow(self.get_flow())
        # 必须包含service 节点
        self.set_must_node_names([self.get_service_name()])
        self.set_flow_name(self.get_flow_name())
        flow_result = self.flow(handler_node)
        return flow_result

    def result(self, params):
        flow = self.get_flow()
        if not flow:
            return self.fail(msg="没有找到" + self.get_flow_name() + "节点，请检查配置")
        flow_result = self.execute(self.handler_current_node)
        if not self.is_success(flow_result):
            return flow_result
        return self.success({})
