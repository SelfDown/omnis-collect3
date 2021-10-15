# -*- coding: utf-8 -*-
"""
@Time: 2021/8/4 9:14
@Author: zzhang zzhang@cenboomh.com
@File: to_json_str.py
@desc:
"""
from collect.service_imp.common.filters.template_filters.base_filter import BaseFilter


class JsonStr(BaseFilter):
    def filter(self, value):
        if not value:
            return ""
        try:
            import json
            return json.dumps(value)
        except Exception as e:
            return value
