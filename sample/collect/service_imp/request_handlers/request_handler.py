# -*- coding: utf-8 -*-
"""
@Time: 2021/7/26 11:25
@Author: zzhang zzhang@cenboomh.com
@File: request_handler.py
@desc:
"""
# -*- coding: utf-8 -*-
from collect.service_imp.result_handlers.result_handler import ResultHandler



class RequestHandler(ResultHandler):
    result_config = {
        'field2array': {
            "path": "collect.service_imp.request_handlers.handlers.field2array",
            "class_name": "Field2Array",
            "method": "handler"
        },
        'service2field': {
            "path": "collect.service_imp.request_handlers.handlers.service2field",
            "class_name": "Service2Field",
            "method": "handler"
        },
        'ignore_data': {
            "path": "collect.service_imp.request_handlers.handlers.ignore_data",
            "class_name": "IgnoreData",
            "method": "handler"
        },
        'update_data': {
            "path": "collect.service_imp.request_handlers.handlers.update_data",
            "class_name": "UpdateData",
            "method": "handler"
        }
    }

    def req_handler(self, params, handler_config, template):
        """
        获取结果处理器,这里做了个中转
        :param handler_config:
        :param result:
        :param template:
        :return:
        """
        return self.handler(params, handler_config, template, handler_type='param')
