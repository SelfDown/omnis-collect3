# -*- coding: utf-8 -*-
"""
@Time: 2021/8/11 14:55
@Author: zzhang zzhang@cenboomh.com
@File: after_plugin.py
@desc:
"""
from collect.service_imp.before_plugin.before_plugin import BeforePlugin


class AfterPlugin(BeforePlugin):

    def handler(self, result, template):

        after_plugin = self.get_after_plugin()
        if not after_plugin:
            return self.success(result)
        from collect.service_imp.common.filters.template_tool import TemplateTool
        tool = TemplateTool(self.op_user)
        msg = ""
        other = None
        for plugin in after_plugin:
            from collect.utils.collect_utils import get_safe_data
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
            plugin_result = method(result, template)
            if not self.is_success(plugin_result) or self.is_finish(plugin_result):
                return plugin_result
            result = self.get_data(plugin_result)
            # 处理消息
            plugin_msg = self.get_msg(plugin_result)
            if plugin_msg:
                msg = plugin_msg
            # 处理其他信息
            other = self.combine_other(other, plugin_result)

        return self.success(result, msg=msg, other=other)
