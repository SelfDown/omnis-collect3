# -*- coding: utf-8 -*-
"""
@Time: 2021/7/22 10:38
@Author: zzhang zzhang@cenboomh.com
@File: row2col.py
@desc:
"""
from collect.service_imp.common.filters.template_tool import TemplateTool
from collect.service_imp.result_handlers.result_handler import ResultHandler
from collect.utils.collect_utils import get_safe_data


class ResultMsg(ResultHandler):
    def handler(self, result, config, template):
        params = get_safe_data(self.get_params_name(), config)
        if not params:
            return self.fail("消息理器没有找到 {params} 节点".format(params=self.get_params_name()))
        params_result = self.get_params_result(template)
        temp = get_safe_data(self.get_template_name(), params)
        tool = self.get_render_tool()
        msg = self.get_render_data(temp, params_result, tool)
        return self.success(result, msg=msg)
