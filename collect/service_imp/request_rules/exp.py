# -*- coding: utf-8 -*-
"""
@Time: 2021/7/1 17:09
@Author: zzhang zzhang@cenboomh.com
@File: format.py
@desc:
"""
from collect.collect_service import CollectService
from collect.utils.collect_utils import get_safe_data


class Expression(CollectService):
    def handler(self, params, config_params, template=None):
        # 计算表达式
        for key in config_params:
            config_param = config_params[key]

            exp = get_safe_data(self.get_exp_name(), config_param)
            if exp:
                try:
                    exp = exp.format(**params)
                    v = eval(exp)
                    params[key] = v
                except Exception as e:
                    return self.fail(msg=str(e) + key + "字段exp有问题")
        return self.success(params)
