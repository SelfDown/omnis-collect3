# -*- coding: utf-8 -*-
"""
@Time: 2021/7/30 20:24
@Author: zzhang zzhang@cenboomh.com
@File: tree_node_name.py
@desc:
"""
from collect.service_imp.result_handlers.result_handler import ResultHandler
from collect.utils.collect_utils import get_safe_data


class TreeNodeName(ResultHandler):
    def handler(self, result, config, template):
        """
        树形节点处理器
        :param result:
        :param config:
        :param template:
        :return:
        """
        params = get_safe_data(self.get_params_name(), config)
        if not params:
            return self.fail("树形节点处理器没有找到 {params} 节点".format(params=self.get_params_name()))
        params_result = self.get_params_result(template)
        tree_name = self.get_tree_name()
        tree_attr_name = get_safe_data(tree_name, params)
        if not tree_attr_name:
            return self.fail("配置params参数中没有找到" + tree_name + "节点")
        tree_arr = get_safe_data(tree_attr_name, params_result)
        if not tree_arr:
            return self.fail("请求参数中没有找到" + tree_attr_name + "属性")

        tree_dict = {}
        tree_id = get_safe_data(self.get_tree_id_name(), params)
        if not tree_id:
            return self.fail("配置params参数中没有找到" + self.get_tree_id_name() + "节点")
        tree_parent = get_safe_data(self.get_tree_parent_name(), params)
        if not tree_parent:
            return self.fail("配置params参数中没有找到" + self.get_tree_parent_name() + "节点")
        field = get_safe_data(self.get_field_name(), params)
        if not field:
            return self.fail("配置params参数中没有找到" + self.get_field_name() + "节点")

        if not self.get_to_field_name() in params:
            return self.fail("配置params参数中没有找到" + self.get_to_field_name() + "节点")
        to_field = params[self.get_to_field_name()]
        templ = get_safe_data(self.get_template_name(), params)
        if not templ:
            return self.fail("配置params参数中没有找到" + self.get_template_name() + "节点")
        if len(tree_arr) <= 0:
            return result
        for tree_item in tree_arr:
            if not tree_id in tree_item:
                return self.fail(tree_arr + "列表中没有找到" + tree_id + "属性")

            if tree_parent not in tree_item:
                return self.fail(tree_arr + "列表中没有找到" + tree_parent + "属性")

            key = tree_item[tree_id]
            tree_dict[key] = tree_item

        from collect.service_imp.common.filters.template_tool import TemplateTool
        tool = TemplateTool(op_user=self.op_user)

        # 获取目标节点
        def get_target_node(node_value):
            current_node = tree_dict[node_value]
            if tree_parent in current_node:
                pid = current_node[tree_parent]
            else:
                pid = ""

            if pid not in tree_dict:
                parent_node = {}
            else:
                parent_node = tree_dict[pid]

            temp_result = tool.render(templ, {'current_node': current_node, "parent_node": parent_node})
            if temp_result == self.get_true_value() or pid not in tree_dict:
                return current_node
            else:
                return get_target_node(pid)

        for result_item in result:
            if field not in result_item:
                return self.fail("结果列表中没有找到" + field + "字段")
            field_value = result_item[field]
            if field_value not in tree_dict:
                for to_field_item in to_field:
                    val_templ = get_safe_data(self.get_value_name(), to_field_item)
                    if not val_templ:
                        return self.fail(self.get_to_field_name() + "中没有找到" + self.get_value_name())
                    field_name_item = get_safe_data(self.get_field_name(), to_field_item)
                    if not field_name_item:
                        return self.fail(self.get_to_field_name() + "中没有找到" + self.get_field_name())
                    result_item[field_name_item] = ""
                continue
            current = tree_dict[field_value]

            if tree_parent not in current:
                return self.fail("结果列表中没有找到" + tree_parent + "字段")

            # 赋值
            current_node = get_target_node(field_value)
            if current_node:
                for to_field_item in to_field:
                    val_templ = get_safe_data(self.get_value_name(), to_field_item)
                    if not val_templ:
                        return self.fail(self.get_to_field_name() + "中没有找到" + self.get_value_name())
                    field_name_item = get_safe_data(self.get_field_name(), to_field_item)
                    if not field_name_item:
                        return self.fail(self.get_to_field_name() + "中没有找到" + self.get_field_name())
                    val = tool.render(val_templ, {'current_node': current_node})
                    result_item[field_name_item] = val

        return self.success(result)
