# -*- coding: utf-8 -*-
"""
@Time: 2021/7/15 15:24
@Author: zzhang zzhang@cenboomh.com
@File: uuid.py
@desc:
"""
from collect.service_imp.common.filters.template_filters.base_filter import BaseFilter


class Md5Filter(BaseFilter):

    @staticmethod
    def filter(value):
        import hashlib
        return hashlib.md5(value.encode(encoding="utf-8")).hexdigest()
