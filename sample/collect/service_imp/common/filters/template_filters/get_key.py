# -*- coding: utf-8 -*-
"""
@Time: 2021/8/3 15:35
@Author: zzhang zzhang@cenboomh.com
@File: conf_key.py
@desc:
"""
from collect.service_imp.common.filters.template_filters.base_filter import BaseFilter
from collect.utils.collect_utils import get_key


class GetKey(BaseFilter):
    def filter(self, value):
        return get_key(value)
