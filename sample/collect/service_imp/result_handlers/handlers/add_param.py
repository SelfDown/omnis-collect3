# -*- coding: utf-8 -*-
"""
@Time: 2021/8/4 11:03
@Author: zzhang zzhang@cenboomh.com
@File: add_param.py
@desc:
"""
from collect.service_imp.result_handlers.result_handler import ResultHandler
from collect.utils.collect_utils import get_safe_data
from collect.service_imp.common.filters.template_tool import TemplateTool

class AddParam(ResultHandler):
    def handler(self, result, config, template):
        param_result = self.get_params_result(template)
        # 来源字段
        from_field_name = self.get_from_field_name()
        params = get_safe_data(self.get_params_name(), config)
        if not params:
            return self.fail("添加列表结果处理器，没有" + self.get_params_name() + "字段")
        from_field = get_safe_data(from_field_name, params)
        # 目标字段
        to_field_name = self.get_to_field_name()
        to_field = get_safe_data(to_field_name, params)
        # if not result:
        #     return self.success(result)
        if from_field in param_result:
            val = param_result[from_field]
        else:
            t = TemplateTool()
            val = t.render(from_field, param_result)
        if isinstance(result, object):
            result[to_field] = val
        elif isinstance(result, list):
            for item in result:
                item[to_field] = val
        return self.success(result)
