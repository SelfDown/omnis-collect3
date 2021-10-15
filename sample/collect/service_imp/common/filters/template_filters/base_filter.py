# -*- coding: utf-8 -*-
"""
@Time: 2021/7/15 15:56
@Author: zzhang zzhang@cenboomh.com
@File: base_filter.py
@desc:
"""
from collect.collect_service import CollectService


class BaseFilter(CollectService):
    def __init__(self, op_user, params, config_params, template,current_key):
        self.params = params
        self.config_params = config_params
        self.op_user = op_user
        self.template = template
        self.current_key = current_key
