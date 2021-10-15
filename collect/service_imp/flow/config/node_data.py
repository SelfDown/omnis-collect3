# -*- coding: utf-8 -*-
"""
@Time: 2021/9/8 9:23
@Author: zzhang zzhang@cenboomh.com
@File: node_data.py
@desc:
"""
from collect.service_imp.flow.config_service import ConfigService
from collect.utils.collect_utils import get_safe_data


class NodeData(ConfigService):
    nd_const = {
        "target_name": "target",
    }

    def get_target_name(self):
        return self.nd_const["target_name"]

    def handler(self, params, config, template):
        target_name = get_safe_data(self.get_target_name(), config)
        if not target_name:
            return self.fail("配置中沒有找到" + self.get_target_name())

        tool = self.get_render_tool()
        params_result = self.get_params_result(template)
        target = self.get_render_data(target_name, params_result, tool)
        result = self.make_service(target)
        if not self.is_success(result):
            return result
        data = self.get_data(result)
        target_template = data.template
        if not target_template:
            return self.fail("没有找到流程服务")
        nodes = None
        for parent_key in target_template:
            parent = target_template[parent_key]
            if not isinstance(parent, dict):
                continue
            for child_key in parent:
                child = parent[child_key]
                if self.get_services_name() == child_key \
                        and isinstance(child, list) \
                        and len(child) > 2 \
                        and self.get_type_name() in child[0]:
                    nodes = child
                    break
        return self.success(nodes)
