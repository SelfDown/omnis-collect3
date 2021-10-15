# -*- coding: utf-8 -*-
"""
@Time: 2021/7/26 15:31
@Author: zzhang zzhang@cenboomh.com
@File: ignoreData.py
@desc:
"""
from collect.service_imp.common.filters.template_tool import TemplateTool
from collect.service_imp.request_handlers.request_handler import RequestHandler
from collect.utils.collect_utils import get_safe_data


class IgnoreData(RequestHandler):
    def handler(self, params, config, template):
        templ = get_safe_data(self.get_template_name(), config)
        if templ:
            remove_list = []

            template_tool = TemplateTool(op_user=self.op_user)
            foreach_name = get_safe_data(self.get_foreach_name(), config)
            if not foreach_name:
                return self.fail(self.get_foreach_name() + "字段配置没有找到")
            foreach = get_safe_data(foreach_name, params)
            for item in foreach:
                result = template_tool.render(templ, item)
                if result == "True":
                    remove_list.append(item)
            for item in remove_list:
                foreach.remove(item)

            if len(foreach) == 0:
                return self.fail("数据已经全部忽略！")
        return self.success(params)
