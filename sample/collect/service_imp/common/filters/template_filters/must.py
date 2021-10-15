# -*- coding: utf-8 -*-
"""
@Time: 2021/7/16 17:41
@Author: zzhang zzhang@cenboomh.com
@File: must_list.py
@desc:
"""
from collect.service_imp.common.filters.template_filters.base_filter import BaseFilter


class MustFilter(BaseFilter):

    def filter(self, value):
        """

        :param value:
        :return:
        """
        if value is None:
            return False
        if isinstance(value, str) and not value.strip():
            return False
        if len(value) == 0:
            return False
        return True
