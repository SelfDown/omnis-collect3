# -*- coding: utf-8 -*-
"""
@Time: 2021/7/22 14:41
@Author: zzhang zzhang@cenboomh.com
@File: array_sort.py
@desc:
"""
from collect.service_imp.result_handlers.result_handler import ResultHandler
from collect.utils.collect_utils import get_safe_data


class ArraySort(ResultHandler):
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
            return self.fail("排序处理器没有找到 {params} 节点".format(params=self.get_params_name()))
        if isinstance(result, list):
            key = get_safe_data(self.get_key_name(), params)
            reverse = False
            if self.get_reverse_name() in params:
                reverse = params[self.get_reverse_name()]
            result.sort(key=lambda x: x[key], reverse=reverse)
        return self.success(result)
