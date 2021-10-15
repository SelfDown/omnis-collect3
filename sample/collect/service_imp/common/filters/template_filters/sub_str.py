# -*- coding: utf-8 -*-
"""
@Time: 2021/8/3 15:35
@Author: zzhang zzhang@cenboomh.com
@File: conf_key.py
@desc:
"""
from collect.service_imp.common.filters.template_filters.base_filter import BaseFilter


class SubStr(BaseFilter):
    def filter(self, value, start=None, end=None):
        if not value:
            return ""
        if not start and end:
            return value[:end]

        if not end and start:
            return value[start:]
        if start and end:
            return value[start:end]

        return value
