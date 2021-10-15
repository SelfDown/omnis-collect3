# -*- coding: utf-8 -*-
"""
@Time: 2021/7/15 15:54
@Author: zzhang zzhang@cenboomh.com
@File: date_time.py
@desc:
"""
from collect.service_imp.common.filters.template_filters.base_filter import BaseFilter


class CurrentDateTime(BaseFilter):

    # @staticmethod
    def filter(self, value):
        from collect.utils.collect_utils import getDateTime
        return getDateTime()
