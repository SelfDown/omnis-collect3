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


class FilterArr(ResultHandler):
    def handler(self, result, config, template):
        params = get_safe_data(self.get_params_name(), config)
        if not params:
            return self.fail("数组处理器没有找到 {params} 节点".format(params=self.get_params_name()))
        templ = get_safe_data(self.get_template_name(), params)
        if not templ:
            return self.fail(
                "数组处理器没有找到 {params} 节点 没有找到{field}".format(params=self.get_params_name(),
                                                           field=self.get_template_name()))
        field = get_safe_data(self.get_field_name(), params)
        # if not field:
        #     return self.fail(
        #         "数组处理器没有找到 {params} 节点 没有找到{field}".format(params=self.get_field_name(),
        #                                                    field=self.get_template_name()))

        data_list = []
        tool = TemplateTool(op_user=self.op_user)
        if not result:
            result = []
        for item in result:
            if not field:

                value = tool.render(templ, item)
                if value == self.get_true_value():
                    data_list.append(item)
            else:
                child_item = []
                if field not in item:
                    return self.fail(field + "字段不存在")
                for child in item[field]:
                    value = tool.render(templ, child)
                    if value == self.get_true_value():
                        child_item.append(child)
                item[field] = child_item
                data_list.append(item)

        return self.success(data_list)
