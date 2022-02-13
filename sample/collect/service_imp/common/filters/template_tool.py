# -*- coding: utf-8 -*-
"""
@Time: 2021/7/16 13:58
@Author: zzhang zzhang@cenboomh.com
@File: template_tool.py
@desc:
"""

from jinja2 import Environment

from collect.collect_service import CollectService

# 全局变量缓存模板信息
_cache = {}


class TemplateTool(CollectService):
    filter_config = {
        "uuid": {
            "path": "collect.service_imp.common.filters.template_filters.uuid",
            "class_name": "UUIDFilter",
            "method": "filter"
        },
        "current_date_time": {
            "path": "collect.service_imp.common.filters.template_filters.date_time",
            "class_name": "CurrentDateTime",
            "method": "filter"
        },
        "exist": {
            "path": "collect.service_imp.common.filters.template_filters.exist",
            "class_name": "ExistFilter",
            "method": "filter"
        },
        "must_list": {
            "path": "collect.service_imp.common.filters.template_filters.must_list",
            "class_name": "MustListFilter",
            "method": "filter"
        },
        "must": {
            "path": "collect.service_imp.common.filters.template_filters.must",
            "class_name": "MustFilter",
            "method": "filter"
        },
        "foreach": {
            "path": "collect.service_imp.common.filters.template_filters.foreach",
            "class_name": "ForeachFilter",
            "method": "filter"
        },
        "in_array": {
            "path": "collect.service_imp.common.filters.template_filters.in_array",
            "class_name": "InArrayFilter",
            "method": "filter"
        }
    }

    def load_filter(self, env, templ, params, config_params, template):
        filter_config = self.get_filter_handler()
        for key in filter_config:

            if isinstance(templ, str) and key not in templ:
                continue
            rule = filter_config[key]
            path = rule[self.get_path_name()]
            class_name = rule[self.get_class_name()]
            import importlib
            filter_factory = importlib.import_module(path)
            rule_obj = getattr(filter_factory, class_name)(params=params,
                                                           config_params=config_params,
                                                           template=template,
                                                           current_key=key,
                                                           op_user=self.op_user)
            method = getattr(rule_obj, rule[self.get_method_name()])
            env.filters[key] = method

    def render(self, templ, params, config_params=None, template=None):
        if not isinstance(templ, str):
            return templ

        if templ in _cache:
            t = _cache[templ]["temp"]
            env = _cache[templ]["env"]
        else:
            env = Environment()
            t = env.from_string(templ)
            _cache[templ] = {"temp": t, "env": env}
        self.load_filter(env, templ, params, config_params, template)
        try:
            result_content = t.render(**params)
        except Exception as e:
            self.log(templ + "运行报错：" + str(e) + " 请检查配置！！！")
            return ""

        data = result_content.strip()
        if data == "None":
            data = ""
        return data
