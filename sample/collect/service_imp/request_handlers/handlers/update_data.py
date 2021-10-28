# -*- coding: utf-8 -*-
"""
@Time: 2021/7/26 15:31
@Author: zzhang zzhang@cenboomh.com
@File: updateData.py
@desc:
"""
from collect.service_imp.common.filters.template_tool import TemplateTool
from collect.service_imp.request_handlers.request_handler import RequestHandler
from collect.utils.collect_utils import get_safe_data


class UpdateData(RequestHandler):
    UDConst = {
        "fields_name": "fields",
        "item_name": "item",

    }

    def get_fields_name(self):
        return self.UDConst["fields_name"]

    def get_item_name(self):
        return self.UDConst["item_name"]

    def handler(self, params, config, template):

        template_tool = TemplateTool(op_user=self.op_user)
        foreach_name = get_safe_data(self.get_foreach_name(), config)
        if not foreach_name:
            return self.fail(self.get_foreach_name() + "字段配置没有找到")
        item_name = get_safe_data(self.get_item_name(), config)
        if not item_name:
            return self.fail(self.get_item_name() + "字段配置没有找到")
        foreach = get_safe_data(foreach_name, params)
        if not foreach:
            return self.fail(foreach_name + "字段参数没有找到")
        fields = get_safe_data(self.get_fields_name(), config)
        if not fields:
            return self.fail(self.get_fields_name() + "字段配置没有找到")
        import copy
        params_copy = copy.deepcopy(params)
        for item in foreach:

            for field in fields:
                temp = get_safe_data(self.get_template_name(), field)
                if not temp:
                    return self.fail(self.get_fields_name() + "没有配置" + self.get_template_name())
                field_name = get_safe_data(self.get_field_name(), field)
                item[field_name] = self.get_render_data(temp, params_copy, template_tool)

        return self.success(params)
