# -*- coding: utf-8 -*-
"""
@Time: 2021/8/28 18:40
@Author: zzhang zzhang@cenboomh.com
@File: get_array_obj.py
@desc:
"""
from collect.service_imp.request_handlers.request_handler import RequestHandler
from collect.utils.collect_utils import get_safe_data


class GetArrayObj(RequestHandler):
    gao_const = {
        "from_array_name": "from_array",
        "to_obj_array_name": "to_obj_array"
    }

    def get_from_array_name(self):
        return self.gao_const["from_array_name"]

    def get_to_obj_array_name(self):
        return self.gao_const["to_obj_array_name"]

    def handler(self, params, config, template):
        params_config = get_safe_data(self.get_params_name(), config)
        if not params_config:
            return self.fail("获取数组对象处理器没有找到 {params} 节点".format(params=self.get_params_name()))
        from_array = get_safe_data(self.get_from_array_name(), params_config)
        if not from_array:
            return self.fail("获取数组对象处理器,没有找到{field}".format(field=self.get_from_array_name()))
        obj_array = get_safe_data(self.get_to_obj_array_name(), params_config)
        if not obj_array:
            return self.fail("获取数组对象处理器,没有找到{field}".format(field=self.get_to_obj_array_name()))

        templ = get_safe_data(self.get_template_name(), params_config)
        if not templ:
            return self.fail("获取数组对象处理器,没有找到{field}".format(field=self.get_template_name()))

        save_field = get_safe_data(self.get_save_field_name(), params_config)
        if not save_field:
            return self.fail("获取数组对象处理器,没有找到{field}".format(field=self.get_save_field_name()))

        from_list = get_safe_data(from_array, params)
        if not isinstance(from_list, list):
            return self.fail("获取数组对象处理器, 请求参数" + from_array + " 不是数组")
        to_list = get_safe_data(obj_array, params)
        if not isinstance(to_list, list):
            return self.fail("获取数组对象处理器, 请求参数" + obj_array + " 不是数组")

        from collect.service_imp.common.filters.template_tool import TemplateTool
        tool = TemplateTool(op_user=self.op_user)
        data_list = []
        for from_item in from_list:
            # val = tool.render(templ, item)
            # result_list.append(val)
            for to_obj in to_list:
                data = {
                    "from_item": from_item,
                    "to_obj": to_obj
                }
                v = tool.render(templ, data)
                if v == self.get_true_value():
                    data_list.append(to_obj)

        params[save_field] = data_list

        return self.success(params)
