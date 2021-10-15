# -*- coding: utf-8 -*-
"""
@Time: 2021/8/12 15:26
@Author: zzhang zzhang@cenboomh.com
@File: level_2.py
@desc:
"""
from collect.service_imp.common.filters.template_tool import TemplateTool
from collect.service_imp.result_handlers.result_handler import ResultHandler
from collect.utils.collect_utils import get_safe_data


class Level2(ResultHandler):
    l2_const = {
        "level_1_fields_name": "level_1_fields",
        "children_field_name": "children_field"
    }

    def get_level_1_fields_name(self):
        return self.l2_const["level_1_fields_name"]

    def get_children_field_name(self):
        return self.l2_const["children_field_name"]

    def handler(self, result, config, template):
        params = get_safe_data(self.get_params_name(), config)
        if not params:
            return self.fail("二级处理器没有找到 {params} 节点".format(params=self.get_params_name()))

        level_1_fields = get_safe_data(self.get_level_1_fields_name(), params)
        if not level_1_fields:
            return self.fail(
                "二级处理器没有找到 {params} 节点 没有找到{field}".format(params=self.get_params_name(),
                                                           field=self.get_level_1_fields_name()))

        children_field = get_safe_data(self.get_children_field_name(), params)

        if not children_field:
            return self.fail(
                "二级处理器没有找到 {params} 节点 没有找到{field}".format(params=self.get_params_name(),
                                                           field=self.get_children_field_name()))
        templ = get_safe_data(self.get_template_name(), params)

        if not templ:
            return self.fail(
                "二级处理器没有找到 {params} 节点 没有找到{field}".format(params=self.get_params_name(),
                                                           field=self.get_template_name()))

        data = {}
        tool = TemplateTool(op_user=self.op_user)
        for item in result:
            key = tool.render(templ, item)
            if key not in data:
                data_item = {
                    children_field: []
                }
                for field in level_1_fields:
                    field_name = get_safe_data(self.get_field_name(), field)
                    templ_value = get_safe_data(self.get_template_name(), field)
                    # if field_name not in item:
                    #     return self.fail("结果集中没有找到" + field_name + "字段")
                    data_item[field_name] = tool.render(templ_value, item)
                data[key] = data_item
            data[key][children_field].append(item)
        data_list = data.values()
        return self.success(data_list)
