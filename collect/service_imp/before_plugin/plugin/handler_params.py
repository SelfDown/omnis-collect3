# -*- coding: utf-8 -*-
"""
@Time: 2021/8/11 14:53
@Author: zzhang zzhang@cenboomh.com
@File: extend_param.py
@desc:
"""
from collect.service_imp.before_plugin.before_plugin import BeforePlugin
from collect.utils.collect_utils import get_safe_data


class HandlerParams(BeforePlugin):
    def handler(self, params, template):
        handler_params = get_safe_data(self.get_handler_params_name(), template)
        params_result = self.get_params_result(template)
        # 处理结果
        if not handler_params:
            return self.success(params)
        tool = self.get_render_tool()
        for handler_config in handler_params:

            # params_result = self.get_params_result(template)
            if not self.is_enable(params_result, handler_config):
                continue

            from collect.service_imp.request_handlers.request_handler import RequestHandler
            h = RequestHandler(op_user=self.op_user)
            result_data = h.req_handler(params_result, handler_config, template)
            if self.is_success(result_data):
                params_result = self.get_data(result_data)
                templ = get_safe_data(self.get_template_name(), handler_config)
                if templ:
                    r = self.get_render_data(templ, params_result, tool)
                    # 显示错误信息,如果值为False,则报错
                    if self.get_false_value() == r:
                        err_msg_templ = get_safe_data(self.get_err_msg_name(), handler_config)
                        r_msg = self.get_render_data(err_msg_templ, params_result, tool)
                        return self.fail(r_msg)

                # get_safe_data(self.get_template_name(),handler_config)
            else:
                return result_data
        self.set_params_result(params_result, template)
        return self.success(params)
