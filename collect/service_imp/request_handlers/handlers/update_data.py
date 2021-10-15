# -*- coding: utf-8 -*-
"""
@Time: 2021/7/26 15:31
@Author: zzhang zzhang@cenboomh.com
@File: ignoreData.py
@desc:
"""
from collect.service_imp.common.filters.template_tool import TemplateTool
from collect.service_imp.request_handlers.request_handler import RequestHandler
from collect.utils.collect_utils import get_safe_data


class UpdateData(RequestHandler):
    def handler(self, params, config, template):
        templ = get_safe_data(self.get_template_name(), config)
        if templ:

            template_tool = TemplateTool(op_user=self.op_user)
            foreach_name = get_safe_data(self.get_foreach_name(), config)
            if not foreach_name:
                return self.fail(self.get_foreach_name() + "字段配置没有找到")
            foreach = get_safe_data(foreach_name, params)
            if not foreach:
                return self.success(params)
            for item in foreach:
                result = template_tool.render(templ, item)
                field = get_safe_data(self.get_field_name(), config)
                item[field] = result

        return self.success(params)
