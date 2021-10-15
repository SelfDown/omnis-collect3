# -*- coding: utf-8 -*-
"""
@Time: 2021/7/26 14:58
@Author: zzhang zzhang@cenboomh.com
@File: service2field.py
@desc:
"""

from collect.service_imp.request_handlers.request_handler import RequestHandler
from collect.utils.collect_utils import get_safe_data


class Service2Field(RequestHandler):
    def handler(self, params, config, template):
        service_data = self.get_node_service(node=config,params=params,template=template,append_param=False)
        if not service_data:
            return service_data
        service = self.get_data(service_data)
        service_result = self.get_service_result(service, template)
        if not self.is_success(service_result):
            return service_result
        save_field = get_safe_data(self.get_save_field_name(), config)
        params[save_field] = self.get_data(service_result)

        # result_template = get_safe_data(self.get_template_name(), config)
        # err_msg = get_safe_data(self.get_err_msg_name(), config)
        # if result_template:
        #     from collect.service_imp.common.filters.template_tool import TemplateTool
        #     template_tool = TemplateTool(op_user=self.op_user)
        #     check = template_tool.render(result_template, params)
        #     if check != self.get_true_value():
        #         return self.fail(err_msg)

        return self.success(params)
