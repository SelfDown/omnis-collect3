# -*- coding: utf-8 -*-
"""
@Time: 2021/8/8 18:11
@Author: zzhang zzhang@cenboomh.com
@File: clocktime.py
@desc:
"""
from collect.service_imp.common.filters.template_filters.base_filter import BaseFilter


class ClockTime(BaseFilter):

    # @staticmethod
    def filter(self, value, fmt="%Y-%m-%d %H:%M:%S"):
        try:
            import time
            return time.strftime(fmt, time.localtime(int(value)))
        except Exception as e:
            pass

        return value
