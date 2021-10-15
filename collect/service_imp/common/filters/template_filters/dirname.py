# -*- coding: utf-8 -*-
"""
@Time: 2021/7/15 15:24
@Author: zzhang zzhang@cenboomh.com
@File: uuid.py
@desc:
"""
from collect.service_imp.common.filters.template_filters.base_filter import BaseFilter
from collect.utils.collect_utils import get_uuid


class DirnameFilter(BaseFilter):

    @staticmethod
    def filter(value):
        import os
        return os.path.dirname(value)
