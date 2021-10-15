# -*- coding: utf-8 -*-
"""
@Time: 2021/8/24 9:02
@Author: zzhang zzhang@cenboomh.com
@File: field2json.py
@desc:
"""
from collect.service_imp.result_handlers.result_handler import ResultHandler
from collect.utils.collect_utils import get_safe_data


class Field2JSONService(ResultHandler):
    def handler(self, result, config, template):
        params = get_safe_data(self.get_params_name(), config)
        # 如果是空对象，直接返回
        if not result:
            return self.success(result)
        if not params:
            return self.fail("JSON服务处理器没有找到 {params} 节点".format(params=self.get_params_name()))

        field = get_safe_data(self.get_field_name(), params)
        for item in result:
            if field in item and item[field]:
                import json
                try:
                    item[field] = json.loads(item[field])
                except Exception as e:
                    continue
        return self.success(result)
