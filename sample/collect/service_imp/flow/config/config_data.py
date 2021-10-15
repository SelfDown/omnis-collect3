# -*- coding: utf-8 -*-
"""
@Time: 2021/9/7 15:52
@Author: zzhang zzhang@cenboomh.com
@File: config_data.py
@desc:
"""
from collect.service_imp.flow.config_service import ConfigService
from collect.utils.collect_utils import get_safe_data


class ConfigData(ConfigService):
    cd_const = {
        "group_icon_name": "group_icon",
        "item_icon_name": "item_icon"
    }

    def get_group_icon_name(self):
        return self.cd_const["group_icon_name"]

    def get_item_icon_name(self):
        return self.cd_const["item_icon_name"]

    def handler(self, params, config, template):
        group_icon_name = get_safe_data(self.get_group_icon_name(), config)
        if not group_icon_name:
            return self.fail("配置中沒有找到" + self.get_group_icon_name())
        item_icon_name = get_safe_data(self.get_item_icon_name(), config)
        if not item_icon_name:
            return self.fail("配置中沒有找到" + self.get_item_icon_name())
        from collect.service_imp.common.filters.template_tool import TemplateTool
        tool = TemplateTool(op_user=self.op_user)
        params_result = self.get_params_result(template)
        group_icon = self.get_render_data(group_icon_name, params_result, tool)
        item_icon = self.get_render_data(item_icon_name, params_result, tool)
        config_data = self.get_config_data()
        tree = []
        count = 0

        def is_flow(service):
            for field_key in service:
                tmp = service[field_key]
                if isinstance(tmp, dict) and "services" in tmp:
                    services_tmp = tmp["services"]
                    if isinstance(services_tmp, list):
                        return True

            return False

        for key in config_data:
            group = {"key": key,
                     "iconSkin": group_icon,
                     "children": []}
            services = config_data[key]
            for child_key in services:
                child = services[child_key]
                child["iconSkin"] = item_icon
                child["service"] = "{key}.{child_key}".format(key=key, child_key=child_key)
                child["is_flow"] = is_flow(child)
                group["children"].append(child)
                count += 1
            tree.append(group)
        return self.success(tree, count=count)
