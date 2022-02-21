# -*- coding: utf-8 -*-
"""
@Time: 2021/7/26 16:20
@Author: zzhang zzhang@cenboomh.com
@File: in_array.py
@desc:
"""
from collect.service_imp.common.filters.template_filters.base_filter import BaseFilter


class IsNumberFilter(BaseFilter):

    def filter(self, value):
        try:
            int(value)
            return True
        except Exception as e:
            return False
