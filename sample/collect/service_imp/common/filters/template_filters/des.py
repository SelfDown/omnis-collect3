# -*- coding: utf-8 -*-
"""
@Time: 2021/7/15 15:24
@Author: zzhang zzhang@cenboomh.com
@File: uuid.py
@desc:
"""
from collect.service_imp.common.filters.template_filters.base_filter import BaseFilter


class DESFilter(BaseFilter):

    @staticmethod
    def filter(value, crypt_type="encrypt"):
        from pyDes import des, PAD_PKCS5, ECB
        from collect.utils.collect_utils import get_key
        DES_SECRET_KEY = get_key('des_key')
        des_wrap = get_key('des_wrap')
        des_obj = des(DES_SECRET_KEY, ECB, DES_SECRET_KEY, padmode=PAD_PKCS5)
        import base64
        if crypt_type == "encrypt":
            if value.startswith(des_wrap):
                return value
            value = value.encode()  # 这里中文要转成字节， 英文好像不用
            secret_bytes = des_obj.encrypt(value)
            return des_wrap + str(base64.b64encode(secret_bytes), encoding="utf-8") + des_wrap
        else:
            if not value:
                value = ""
            value = value.replace(des_wrap, "")
            return str(des_obj.decrypt(base64.b64decode(value)),encoding="utf-8")
