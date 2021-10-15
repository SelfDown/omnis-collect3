# -*- coding: utf-8 -*-
"""
@Time: 2021/8/24 10:39
@Author: zzhang zzhang@cenboomh.com
@File: current_day.py
@desc:
"""
from collect.service_imp.common.filters.template_filters.base_filter import BaseFilter


class CurrentDay(BaseFilter):

    # @staticmethod
    def filter(self, value):
        import time
        return time.strftime("%Y-%m-%d", time.localtime())