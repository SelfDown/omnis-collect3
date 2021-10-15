# -*- coding: utf-8 -*-
"""
@Time: 2021/7/1 17:09
@Author: zzhang zzhang@cenboomh.com
@File: format.py
@desc:
"""
from collect.service_imp.common.filters.template_tool import TemplateTool
from collect.service_imp.request_rules.base_rule import BaseRule
from collect.utils.collect_utils import get_safe_data


class TemplateData(BaseRule):

    def handler(self, params, config_params, template=None):
        # 计算format
        for key in config_params:

            config_param = config_params[key]
            # templ = get_safe_data(self.get_template_name(), config_param)
            if self.has_template_str(config_param):

                value_result = self.get_node_template_result(config_param, params, config_params=config_params,
                                                      template=template)
                # template_tool = TemplateTool(op_user=self.op_user)
                # value = template_tool.render(templ, params, config_params, template)
                if not self.is_success(value_result):
                    return value_result
                value = self.get_data(value_result)
                if value is not None:
                    params[key] = value
        return self.success(params)
