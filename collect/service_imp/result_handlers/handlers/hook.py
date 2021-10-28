# -*- coding: utf-8 -*-
"""
@Time: 2021/8/4 16:51
@Author: zzhang zzhang@cenboomh.com
@File: value_arr.py
@desc:
"""
from collect.service_imp.common.filters.template_tool import TemplateTool
from collect.service_imp.result_handlers.result_handler import ResultHandler
from collect.utils.collect_utils import get_safe_data


class Hook(ResultHandler):
    h_const = {
        "result_name": "result_name",
        "children_field_name": "children_field"
    }

    def get_result_name(self):
        return self.h_const["result_name"]

    def handler(self, result, config, template):
        params = get_safe_data(self.get_params_name(), config)
        if not params:
            return self.fail("Hook处理器没有找到 {params} 节点".format(params=self.get_params_name()))

        result_name = get_safe_data(self.get_result_name(), params)
        if not result_name:
            return self.fail("Hook 处理器没有找到" + self.get_result_name() + "参数")

        service_node = get_safe_data(self.get_service_name(), params)
        if not service_node:
            return self.fail("Hook 处理器没有找到" + self.get_service_name() + "参数")
        params_result = self.get_params_result(template)
        params_result[result_name] = result
        service = self.get_node_service(params, params_result)
        if not self.is_success(service):
            return self.fail(service)

        service = self.get_data(service)

        def handler_service(target_service, target_template):
            service_result = self.get_service_result(target_service, target_template)
            if self.is_success(service_result):
                self.log(self.get_msg(service_result), "error")

        # 异步执行线程
        import threading
        t = threading.Thread(target=handler_service, args=(service, template))
        t.start()

        return self.success(result)
