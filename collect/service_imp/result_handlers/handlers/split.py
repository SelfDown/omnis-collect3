# -*- coding: utf-8 -*-
"""
@Time: 2021/7/22 10:38
@Author: zzhang zzhang@cenboomh.com
@File: row2col.py
@desc:
"""
from collect.service_imp.common.filters.template_tool import TemplateTool
from collect.service_imp.result_handlers.result_handler import ResultHandler
from collect.utils.collect_utils import get_safe_data


class Split(ResultHandler):
    s_const = {
        "split_name": "split"
    }

    def get_split_name(self):
        return self.s_const["split_name"]

    def handler(self, result, config, template):
        """
        列转处理器
        :param result:
        :param config:
        :param template:
        :return:
        """
        params = get_safe_data(self.get_params_name(), config)

        if not params:
            return self.fail("分割处理器没有找到 {params} 节点".format(params=self.get_params_name()))

        split = get_safe_data(self.get_split_name(), params)
        if not split:
            return self.fail("参数中没有找到" + self.get_split_name())

        field = get_safe_data(self.get_field_name(), params)
        if not field:
            return self.fail("参数中没有找到" + self.get_field_name())

        def handler_split(item):
            val = get_safe_data(field, item)
            if not val:
                return
            if isinstance(val, str):
                item[field] = val.split(split)

        if isinstance(result, list):
            for item in result:
                handler_split(item)
        else:
            handler_split(result)

        return self.success(result)
