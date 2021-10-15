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


class ValueArr(ResultHandler):
    def handler(self, result, config, template):
        params = get_safe_data(self.get_params_name(), config)
        if not params:
            return self.fail("数组值处理器没有找到 {params} 节点".format(params=self.get_params_name()))
        templ = get_safe_data(self.get_template_name(), params)
        if not templ:
            return self.fail(
                "数组值处理器没有找到 {params} 节点 没有找到{field}".format(params=self.get_params_name(),
                                                            field=self.get_template_name()))

        if not result:
            return self.success(result)
        if not isinstance(result, list):
            return self.success(result)

        tool = TemplateTool(op_user=self.op_user)
        params_result = self.get_params_result(template)
        field = get_safe_data(self.get_field_name(), params)

        def get_temp_value(item):
            # item[self.get_params_result_name()] = params_result
            # value = tool.render(templ, item)
            value = self.get_render_data(templ, item, tool)
            return value
        def add_value(value,data_list):
            if value != "":
                if isinstance(value, list):
                    data_list += value
                else:
                    data_list.append(value)
            return data_list

        if not field:
            data_list = []
            for item in result:
                # item[self.get_params_result_name()] = params_result
                value = get_temp_value(item)
                data_list = add_value(value,data_list)
                # if value != "":
                #     data_list.append(value)
            return self.success(data_list)
        else:
            for item in result:
                data_list = []
                if field in item and isinstance(item[field], list):

                    for child in item[field]:
                        # child[self.get_params_result_name()] = params_result
                        value = get_temp_value(child)
                        data_list = add_value(value, data_list)
                item[field] = data_list
            return self.success(result)
