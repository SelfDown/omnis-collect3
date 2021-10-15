# -*- coding: utf-8 -*-
"""
@Time: 2021/8/11 14:53
@Author: zzhang zzhang@cenboomh.com
@File: extend_param.py
@desc:
"""
from collect.service_imp.before_plugin.before_plugin import BeforePlugin


class HandlerReqCountParam(BeforePlugin):
    def handler(self, params, template):
        params_result= self.get_params_result(template)
        # 设置统计参数
        count_params_result = self.handler_req_count_params(params, params_result,template)
        if not self.is_success(count_params_result):
            return count_params_result
        count_params_result_data = self.get_data(count_params_result)
        self.set_count_params_result(count_params_result_data,template)
        return count_params_result
