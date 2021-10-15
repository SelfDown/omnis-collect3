# -*- coding: utf-8 -*-
"""
@Time: 2021/7/16 17:41
@Author: zzhang zzhang@cenboomh.com
@File: must_list.py
@desc:
"""
from collect.service_imp.common.filters.template_filters.base_filter import BaseFilter


class MustListFilter(BaseFilter):

    def filter(self, value):
        """

        :param value:
        :return:
        """
        if value is None:
            return False
        if not isinstance(value, list):
            return False
        if len(value) == 0:
            return False
        return True
