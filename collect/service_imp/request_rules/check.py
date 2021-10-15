# -*- coding: utf-8 -*-
"""
@Time: 2021/7/16 14:34
@Author: zzhang zzhang@cenboomh.com
@File: check.py
@desc:
"""
from collect.service_imp.request_rules.base_rule import BaseRule
from collect.utils.collect_utils import get_safe_data


class CheckData(BaseRule):
    def handler(self, params, config_params, template=None):
        """

        :param params:
        :param config_params:
        :param template:
        :return:
        """
        # check
        for key in config_params:
            config_param = config_params[key]

            check = get_safe_data(self.get_check_name(), config_param)
            if check:
                result = self.handler_node(key, check, params, config_params, template, check=True)
                if not self.is_success(result):
                    return result
        return self.success(params)
