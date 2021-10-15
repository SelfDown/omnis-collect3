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


class Row2Col(ResultHandler):
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
            return self.fail("行转列处理器没有找到 {params} 节点".format(params=self.get_params_name()))
        field = get_safe_data(self.get_field_name(), params)
        remove = get_safe_data(self.get_remove_name(), params)
        if field:
            t = TemplateTool()
            for item in result:
                col = item[field]
                templ = get_safe_data(self.get_template_name(), params)
                if not templ:
                    return self.fail("行转列处理器{params}没有找到 {template} 节点".format(params=self.get_params_name(),
                                                                               template=self.get_template_name()))

                value = t.render(templ, item)
                item[col] = value
        if remove:
            for item in result:
                for field in remove:
                    if field in item:
                        del item[field]
        return self.success(result)
