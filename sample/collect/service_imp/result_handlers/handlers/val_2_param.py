# -*- coding: utf-8 -*-
"""
@Time: 2021/8/9 16:59
@Author: zzhang zzhang@cenboomh.com
@File: val_2_param.py
@desc:
"""
from collect.service_imp.result_handlers.result_handler import ResultHandler
from collect.utils.collect_utils import get_safe_data


class Val2Param(ResultHandler):
    def handler(self, result, config, template):

        params = get_safe_data(self.get_params_name(), config)
        # 如果是空对象，直接返回
        if not result:
            return self.success(result)
        if not params:
            return self.fail("值转参数处理器没有找到 {params} 节点".format(params=self.get_params_name()))
        templ = get_safe_data(self.get_template_name(), params)
        if not templ:
            return self.fail(
                "值转参数处理器没有找到 {params} 节点 没有找到{field}".format(params=self.get_params_name(),
                                                             field=self.get_template_name()))
        to_field = get_safe_data(self.get_to_field_name(), params)
        if not to_field:
            return self.fail(
                "值转参数处理器没有找到 {params} 节点 没有找到{field}".format(params=self.get_params_name(),
                                                             field=self.get_to_field_name()))
        from collect.service_imp.common.filters.template_tool import TemplateTool
        tool = TemplateTool(op_user=self.op_user)
        param_result = self.get_params_result(template)
        if isinstance(result, dict):
            param_result[to_field] = tool.render(templ, result)
        elif isinstance(result, list):
            data = []
            for item in result:
                data.append(tool.render(templ, item))
            param_result[to_field] = data
        return self.success(result)
