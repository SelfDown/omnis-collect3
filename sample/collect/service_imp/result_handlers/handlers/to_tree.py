# -*- coding: utf-8 -*-
"""
@Time: 2021/8/4 16:51
@Author: zzhang zzhang@cenboomh.com
@File: value_arr.py
@desc:
"""
from collect.service_imp.common.filters.template_tool import TemplateTool
from collect.service_imp.result_handlers.result_handler import ResultHandler
from collect.utils.collect_utils import get_safe_data, listToTree


class ToTree(ResultHandler):
    tt_const = {
        "id_field_name": "id_field",
        "parent_id_field_name": "parent_id_field",
        "children_field_name": "children_field"
    }

    def get_id_field_name(self):
        return self.tt_const["id_field_name"]

    def get_parent_id_field_name(self):
        return self.tt_const["parent_id_field_name"]

    def get_children_field_name(self):
        return self.tt_const["children_field_name"]

    def handler(self, result, config, template):
        params = get_safe_data(self.get_params_name(), config)
        if not params:
            return self.fail("树形处理器没有找到 {params} 节点".format(params=self.get_params_name()))
        id_field = get_safe_data(self.get_id_field_name(), params)
        if not id_field:
            return self.fail(
                "树形处理器没有找到 {params} 节点 没有找到{field}".format(params=self.get_params_name(),
                                                           field=self.get_id_field_name()))

        parent_id_field = get_safe_data(self.get_parent_id_field_name(), params)
        if not parent_id_field:
            return self.fail(
                "树形处理器没有找到 {params} 节点 没有找到{field}".format(params=self.get_params_name(),
                                                           field=self.get_parent_id_field_name()))
        children_field = get_safe_data(self.get_children_field_name(), params)
        if not children_field:
            return self.fail(
                "树形处理器没有找到 {params} 节点 没有找到{field}".format(params=self.get_params_name(),
                                                           field=self.get_children_field_name()))

        tree = listToTree(result, id_field, parent_id_field, children_field)
        return self.success(tree)
