# -*- coding: utf-8 -*-
"""
@Time: 2021/8/11 14:53
@Author: zzhang zzhang@cenboomh.com
@File: extend_param.py
@desc:
"""
from collect.service_imp.before_plugin.before_plugin import BeforePlugin
from collect.utils.collect_utils import get_safe_data


class ExtendParam(BeforePlugin):
    ep_const = {
        "extend_param_name": "extend_param",
        "extend_param_fields_name": "extend_param_fields"
    }

    def get_extend_param_name(self):
        return self.ep_const["extend_param_name"]

    def extend_param_fields_name(self):
        return self.ep_const["extend_param_fields_name"]

    def handler(self, params, template):
        # self.log("进去添加参数插件")

        extend_param_service = get_safe_data(self.get_extend_param_name(), template)
        from collect.collect_service import CollectService
        collect_service = CollectService(op_user=self.op_user)
        result = collect_service.make_service(extend_param_service)
        if not self.is_success(result):
            return result
        extend_service = self.get_data(result)
        extend_template = extend_service.template
        config_params = self.get_config_params(extend_template)
        if not config_params:
            return self.success(params)
        current_config_params = self.get_config_params(template)
        fields = get_safe_data(self.extend_param_fields_name(), template)
        exclude = []
        if fields:
            config_exclude = get_safe_data(self.get_exclude_name(), fields)
            if config_exclude:
                exclude = config_exclude

        for config_param_key in config_params:
            config_param = config_params[config_param_key]
            if config_param_key in exclude or config_param_key in current_config_params:
                continue
            current_config_params[config_param_key] = config_param
        self.set_config_params(current_config_params, template)
        return self.success(params)
