# -*- coding: utf-8 -*-
"""
@Time: 2021/8/11 14:53
@Author: zzhang zzhang@cenboomh.com
@File: extend_param.py
@desc:
"""
from collect.service_imp.before_plugin.before_plugin import BeforePlugin


class HandlerReqParam(BeforePlugin):
    def handler(self, params, template):
        params_result = self.handler_req_params(params,template)
        if not self.is_success(params_result):
            return params_result
        params_result_data = self.get_data(params_result)
        self.set_params_result(params_result_data,template)
        return params_result
