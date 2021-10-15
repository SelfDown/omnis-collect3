# -*- coding: utf-8 -*-
"""
@Time: 2021/8/9 16:59
@Author: zzhang zzhang@cenboomh.com
@File: val_2_param.py
@desc:
"""
from collect.service_imp.result_handlers.result_handler import ResultHandler
from collect.utils.collect_utils import get_safe_data


class Param2Result(ResultHandler):
    def handler(self, result, config, template):

        params = get_safe_data(self.get_params_name(), config)
        if not params:
            return self.fail("值转参数处理器没有找到 {params} 节点".format(params=self.get_params_name()))
        field = get_safe_data(self.get_field_name(), params)
        if not field:
            return self.fail(
                "值转参数处理器没有找到 {params} 节点 没有找到{field}".format(params=self.get_params_name(),
                                                             field=self.get_field_name()))


        result = get_safe_data(field, self.get_params_result(template))
        return self.success(result)
