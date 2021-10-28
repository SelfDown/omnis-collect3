# -*- coding: utf-8 -*-
"""
@Time: 2021/7/26 16:20
@Author: zzhang zzhang@cenboomh.com
@File: in_array.py
@desc:
"""
from collect.service_imp.common.filters.template_filters.base_filter import BaseFilter


class IsEmptyFilter(BaseFilter):

    def filter(self, value, obj=None):
        if obj is not None:
            from collect.utils.collect_utils import get_safe_data
            value = get_safe_data(value, obj, False)
        if value:
            return False
        else:
            return True
