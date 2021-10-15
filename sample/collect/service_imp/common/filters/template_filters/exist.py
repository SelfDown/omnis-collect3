# -*- coding: utf-8 -*-
"""
@Time: 2021/7/16 15:03
@Author: zzhang zzhang@cenboomh.com
@File: exist.py
@desc:
"""
from collect.service_imp.common.filters.template_filters.base_filter import BaseFilter


class ExistFilter(BaseFilter):

    def filter(self, value, field_key=None):
        """

        :param value:
        :return:
        """
        model_obj = self.get_model_obj()
        if not self.is_success(model_obj):
            return False
        model = self.get_model_class()
        f = {field_key: value}
        if len(model.objects.filter(**f)) > 0:
            return True
        else:
            return False
