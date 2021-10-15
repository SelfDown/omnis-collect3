# -*- coding: utf-8 -*-
"""
@Time: 2021/8/9 17:46
@Author: zzhang zzhang@cenboomh.com
@File: combine_service.py
@desc:
"""
from collect.service_imp.common.filters.template_tool import TemplateTool
from collect.service_imp.result_handlers.result_handler import ResultHandler
from collect.utils.collect_utils import get_safe_data


class CombineService(ResultHandler):
    cs_const = {
        "multiple_name": "multiple"
    }

    def get_multiple_name(self):
        return self.cs_const["multiple_name"]

    def handler(self, result, config, template):
        params = get_safe_data(self.get_params_name(), config)
        # 如果是空对象，直接返回
        if not result:
            return self.success(result)
        if not params:
            return self.fail("结合服务处理器没有找到 {params} 节点".format(params=self.get_params_name()))

        service = get_safe_data(self.get_service_name(), params)
        if not service:
            return self.fail(
                "结合服务处理器没有找到 {params} 节点 没有找到{field}".format(params=self.get_params_name(),
                                                             field=self.get_service_name()))

        from_field = get_safe_data(self.get_from_field_name(), params)
        if not from_field:
            return self.fail(
                "结合服务处理器没有找到 {params} 节点 没有找到{field}".format(params=self.get_params_name(),
                                                             field=self.get_from_field_name()))

        to_field = get_safe_data(self.get_to_field_name(), params)
        if not to_field:
            return self.fail(
                "结合服务处理器没有找到 {params} 节点 没有找到{field}".format(params=self.get_params_name(),
                                                             field=self.get_to_field_name()))

        save_field = get_safe_data(self.get_save_field_name(), params)
        if not save_field:
            return self.fail(
                "结合服务处理器没有找到 {params} 节点 没有找到{field}".format(params=self.get_params_name(),
                                                             field=self.get_save_field_name()))

        multiple = get_safe_data(self.get_multiple_name(), params)
        # template_tool = TemplateTool(op_user=self.op_user)
        # params_result = self.get_params_result(template)
        # for key in service:
        #     value_template = service[key]
        #     # 如果配置的值存在，参数中，就取参数
        #     if value_template in params_result:
        #         value = params_result[value_template]
        #     else:
        #         value = template_tool.render(value_template, params_result)
        #     service[key] = value
        # for key in params_result:
        #     if key not in service:
        #         service[key] = params_result[key]
        params_result = self.get_params_result(template)
        s_result = self.get_node_service(params, params=params_result,template=template, append_param=True)
        if not self.is_success(s_result):
            return s_result
        service = self.get_data(s_result)
        service_result = self.get_service_result(service, template)
        if not self.is_success(service_result):
            return service_result
        service_result = self.get_data(service_result)
        if not service_result:
            service_result = []
        service_result_dict = {}
        for item in service_result:
            if from_field not in item:
                continue
            val_key = item[from_field]
            if multiple:
                if val_key not in service_result_dict:
                    service_result_dict[val_key] = []
                service_result_dict[val_key].append(item)
            else:
                service_result_dict[val_key] = item

        for item in result:
            if to_field not in item:
                continue
            val_key = item[to_field]
            if val_key not in service_result_dict:
                item[save_field] = {}
                continue
            item[save_field] = service_result_dict[val_key]

        return self.success(result)
