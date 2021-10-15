# -*- coding: utf-8 -*-
"""
@Time: 2021/8/11 14:55
@Author: zzhang zzhang@cenboomh.com
@File: before_plugin.py
@desc:
"""
from collect.collect_service import CollectService
from collect.utils.collect_utils import get_safe_data


class BeforePlugin(CollectService):
    def handler(self, params, template):
        before_plugin = self.get_before_plugin()
        if not before_plugin:
            return self.success(params)
        from collect.service_imp.common.filters.template_tool import TemplateTool
        tool = TemplateTool(self.op_user)
        for plugin in before_plugin:
            templ = get_safe_data(self.get_template_name(), plugin)
            v = tool.render(templ, template)
            if v != self.get_true_value():
                continue
            path = plugin[self.get_path_name()]
            class_name = plugin[self.get_class_name()]
            try:
                import importlib
                result_factory = importlib.import_module(path)
                result_obj = getattr(result_factory, class_name)(op_user=self.op_user)
                method = getattr(result_obj, plugin[self.get_method_name()])
            except Exception as e:
                return self.fail(class_name + "找不到，请检查配置" + str(e))
            plugin_result = method(params, template)
            if not self.is_success(plugin_result) or self.is_finish(plugin_result):
                return plugin_result
            params = self.get_data(plugin_result)

        return self.success(params)
