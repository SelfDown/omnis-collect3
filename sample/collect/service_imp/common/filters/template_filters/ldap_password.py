# -*- coding: utf-8 -*-
"""
@Time: 2021/7/15 15:24
@Author: zzhang zzhang@cenboomh.com
@File: uuid.py
@desc:
"""
from collect.service_imp.common.filters.template_filters.base_filter import BaseFilter
from collect.utils.collect_utils import get_uuid


class LdapPasswordFilter(BaseFilter):

    @staticmethod
    def filter(value):
        from ldap3 import HASHED_SALTED_SHA
        from ldap3.utils.hashed import hashed
        hashed_password = hashed(HASHED_SALTED_SHA, value)
        return hashed_password
