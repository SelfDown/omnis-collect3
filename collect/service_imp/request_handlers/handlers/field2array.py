# -*- coding: utf-8 -*-
"""
@Time: 2021/7/26 11:31
@Author: zzhang zzhang@cenboomh.com
@File: field2array.py
@desc:
"""
from collect.service_imp.request_handlers.request_handler import RequestHandler
from collect.utils.collect_utils import get_safe_data


class Field2Array(RequestHandler):
    def handler(self, params, config, template):
        """
        字段转对象数组
        :param params:
        :param config:
        :param template:
        :return:
        """
        from_field_name = get_safe_data(self.get_from_field_name(), config)
        if not from_field_name:
            return self.fail(self.get_from_field_name() + "字段配置不存在")

        from_field = get_safe_data(from_field_name, params)
        if not from_field:
            return self.fail(self.get_from_field_name() + "不能为空")
        to_field = get_safe_data(self.get_to_field_name(), config)
        save_field = get_safe_data(self.get_save_field_name(), config)
        l = []
        for obj_id in from_field:
            import copy
            p_tmp = copy.copy(params)
            p_tmp[to_field] = obj_id
            del p_tmp[from_field_name]
            l.append(p_tmp)
        params[save_field] = l
        return self.success(params)
