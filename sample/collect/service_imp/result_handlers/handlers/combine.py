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


class Combine(ResultHandler):
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
            return self.fail("合并处理器没有找到 {params} 节点".format(params=self.get_params_name()))
        templ = get_safe_data(self.get_template_name(), params)
        if not templ:
            return self.fail("合并列处理器{params}没有找到 {template} 节点".format(params=self.get_params_name(),
                                                                       template=self.get_template_name()))
        key_dict = {}

        t = TemplateTool()
        for item in result:
            key = t.render(templ, item)
            if key in key_dict:
                key_obj = key_dict[key]
            else:
                key_obj = {}
            key_obj = dict(key_obj.items() + item.items())
            key_dict[key] = key_obj
        result = key_dict.values()
        return self.success(result)
