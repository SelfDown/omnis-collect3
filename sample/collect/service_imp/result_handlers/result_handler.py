# -*- coding: utf-8 -*-
"""
@Time: 2021/7/22 10:32
@Author: zzhang zzhang@cenboomh.com
@File: result_handler.py
@desc:
"""
from collect.collect_service import CollectService
from collect.utils.collect_utils import get_safe_data


class ResultHandler(CollectService):
    result_config = {
        "row2col": {
            "path": "collect.service_imp.result_handlers.handlers.row2col",
            "class_name": "Row2Col",
            "method": "handler"
        },
        "combine": {
            "path": "collect.service_imp.result_handlers.handlers.combine",
            "class_name": "Combine",
            "method": "handler"
        },
        "arrsort": {
            "path": "collect.service_imp.result_handlers.handlers.array_sort",
            "class_name": "ArraySort",
            "method": "handler"
        }
    }

    def handler(self, result, handler_config, template, handler_type='result'):
        """
        获取结果处理器,这里做了个中转
        :param handler_config:
        :param result:
        :param template:
        :param handler_type: result 表示结果处理，request 请求处理器
        :return:
        """
        config = get_safe_data(self.get_key_name(), handler_config)
        if handler_type == "result":
            config_handler = self.get_result_handler()
        else:
            config_handler = self.get_request_handler()
        if config not in config_handler:
            if handler_type == 'result':
                return self.fail('{key} 结果处理器不存在'.format(key=config))
            else:
                return self.fail('{key} 请求处理器不存在'.format(key=config))
        config_data = config_handler[config]
        path = config_data[self.get_path_name()]
        class_name = config_data[self.get_class_name()]
        try:
            import importlib
            result_factory = importlib.import_module(path)
            result_obj = getattr(result_factory, class_name)(op_user=self.op_user)
            method = getattr(result_obj, config_data[self.get_method_name()])
        except Exception as e:
            return self.fail(class_name + "找不到，请检查配置" + str(e))
        return method(result, handler_config, template)
