# -*- coding: utf-8 -*-
"""
@Time: 2021/7/1 17:09
@Author: zzhang zzhang@cenboomh.com
@File: format.py
@desc:
"""
from collect.collect_service import CollectService
from collect.utils.collect_utils import get_safe_data


class Format(CollectService):
    def handler(self, params, config_params, template=None):

        # 计算format
        for key in config_params:
            config_param = config_params[key]

            if not config_param:
                return self.fail(msg=key + "字段 ，format 规则不存在配置")
            exp = get_safe_data(self.get_format_name(), config_param)
            if exp:
                try:
                    v = exp.format(**params)
                    if v:
                        v = v.strip()
                    params[key] = v
                except Exception as e:
                    return self.fail(msg=str(e) + "字段 ，format 规则 有问题")

        return self.success(params)
