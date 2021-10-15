# -*- coding: utf-8 -*-
"""
@Time: 2021/9/8 9:23
@Author: zzhang zzhang@cenboomh.com
@File: node_data.py
@desc:
"""
from collect.service_imp.flow.config_service import ConfigService
from collect.utils.collect_utils import get_safe_data


class InitNode(ConfigService):
    in_const = {

        "node_name": "node",
        "height_name": "height",
        "width_name": "width",
        "start_x_name": "start_x",
        "start_y_name": "start_y",
        "x_distance_name": "x_distance",
        "y_distance_name": "y_distance",
        "condition_name": "condition"

    }

    def get_condition_name(self):
        return self.in_const["condition_name"]

    def get_node_name(self):
        return self.in_const["node_name"]

    def get_x_distance_name(self):
        return self.in_const["x_distance_name"]

    def get_y_distance_name(self):
        return self.in_const["y_distance_name"]

    def get_height_name(self):
        return self.in_const["height_name"]

    def get_width_name(self):
        return self.in_const["width_name"]

    def get_start_x_name(self):
        return self.in_const["start_x_name"]

    def get_start_y_name(self):
        return self.in_const["start_y_name"]

    def get_template_nodes(self, templ):
        if not templ:
            return []
        from jinja2 import Environment
        env = Environment()
        parsed_content = env.parse(templ)
        content = parsed_content.body
        result = []

        def get_node(node):
            node_list = []
            if hasattr(node, "nodes"):
                nodes = getattr(node, "nodes")
                for node in nodes:
                    data = getattr(node, "data")
                    node_list.append(data.strip())
            for l in "body", "elif_", "else_":
                node_list += get_nodes(node, l)
            return node_list

        def get_nodes(parent_node, name):
            node_list = []
            if not hasattr(parent_node, name):
                return node_list
            body = getattr(parent_node, name)
            for child in body:
                node_list += get_node(child)
            return node_list

        for item in content:
            result += get_node(item)
        return result

    def handler(self, params, config, template):
        node_name = get_safe_data(self.get_node_name(), config)
        if not node_name:
            return self.fail("配置中沒有找到" + self.get_node_name())
        height_name = get_safe_data(self.get_height_name(), config)
        if not height_name:
            return self.fail("配置中沒有找到" + self.get_height_name())
        width_name = get_safe_data(self.get_width_name(), config)
        if not width_name:
            return self.fail("配置中沒有找到" + self.get_width_name())
        start_x_name = get_safe_data(self.get_start_x_name(), config)
        if not start_x_name:
            return self.fail("配置中沒有找到" + self.get_start_x_name())

        start_y_name = get_safe_data(self.get_start_y_name(), config)
        if not start_y_name:
            return self.fail("配置中沒有找到" + self.get_start_y_name())

        x_distance_name = get_safe_data(self.get_x_distance_name(), config)
        if not x_distance_name:
            return self.fail("配置中沒有找到" + self.get_x_distance_name())

        y_distance_name = get_safe_data(self.get_y_distance_name(), config)
        if not y_distance_name:
            return self.fail("配置中沒有找到" + self.get_y_distance_name())

        tool = self.get_render_tool()
        params_result = self.get_params_result(template)
        nodes = self.get_render_data(node_name, params_result, tool)
        if not nodes:
            return self.fail("参数中没有找到" + node_name)
        width = self.get_render_data(width_name, params_result, tool)
        if not width:
            return self.fail("参数中没有找到" + width_name)
        height = self.get_render_data(height_name, params_result, tool)
        if not height:
            return self.fail("参数中没有找到" + height_name)
        start_x = self.get_render_data(start_x_name, params_result, tool)
        if not width:
            return self.fail("参数中没有找到" + start_x)
        start_y = self.get_render_data(start_y_name, params_result, tool)
        if not start_y:
            return self.fail("参数中没有找到" + start_y_name)
        x_distance = self.get_render_data(x_distance_name, params_result, tool)
        y_distance = self.get_render_data(y_distance_name, params_result, tool)
        node_dict = {}
        for node in nodes:
            key = get_safe_data(self.get_key_name(), node)
            node_dict[key] = node
        parse_node_dict = {}

        def get_node_data(node_key):
            node_key = node_key.strip()
            return get_safe_data(node_key, parse_node_dict)

        for key in node_dict:
            node = node_dict[key]
            next = get_safe_data(self.get_next_name(), node)
            next_node_keys = self.get_template_nodes(next)
            if len(next_node_keys) <= 1:
                parse_node_dict[key] = node
                continue

            import copy
            condition = copy.deepcopy(node)
            condition_name = self.get_condition_name()
            new_key = key + "_" + condition_name
            condition[self.get_type_name()] = condition_name
            condition[self.get_key_name()] = new_key
            condition["desc"] = condition[self.get_next_name()]
            condition[self.get_name_name()] = "智能条件"
            condition[self.get_next_name()] = next_node_keys
            node[self.get_next_name()] = new_key
            parse_node_dict[key] = node
            parse_node_dict[new_key] = condition

        target_node_dict = {}

        # current_node = self.get_start_node(parse_node_dict)
        # start_key = get_safe_data(self.get_key_name(), current_node)
        def get_target_node(node):
            desc = get_safe_data("desc", node)
            if not desc:
                desc = get_safe_data(self.get_name_name(), node)
            target = {
                'id': get_safe_data(self.get_key_name(), node),
                'width': width,
                'height': height,
                'coordinate': [get_safe_data("x", node, 0), get_safe_data("y", node, 0)],
                'meta': {
                    'prop': get_safe_data(self.get_type_name(), node),
                    'name': get_safe_data(self.get_name_name(), node),
                    'desc': desc
                }
            }
            return target

        def handler_target_node(key, parent, node_y=None, node_x=None):
            # key = key.strip()
            current = get_node_data(key)
            if "x" in current:
                return
            # 设置首节点的坐标
            if not parent:
                x = start_x
                y = start_y
            else:
                parent_node = get_node_data(parent)
                x = get_safe_data("x", parent_node, 0)
                y = get_safe_data("y", parent_node, 0)
                x += x_distance
            if node_x is not None:
                x = node_x

            current["x"] = x

            if node_y is not None:
                y = node_y
            elif current[self.get_type_name()] == "end":
                y = start_y
            current["y"] = y
            next = get_safe_data(self.get_next_name(), current)
            fail = get_safe_data(self.get_fail_name(), current)

            # 处理正常流程
            if isinstance(next, str):
                handler_target_node(next, get_safe_data(self.get_key_name(), current))
            elif isinstance(next, list):
                unit = y_distance
                node_start_y = y - unit * 2 / 2
                # node_start_y = y - distance * len(next) / 2
                for index, child in enumerate(next):
                    node_y = node_start_y + unit * index
                    if node_y >= y:
                        node_y += unit
                    handler_target_node(child, get_safe_data(self.get_key_name(), current), node_y)

            # 处理失败流程
            if isinstance(fail, str):
                handler_target_node(fail, get_safe_data(self.get_key_name(), current),
                                    node_y=y + y_distance,
                                    node_x=get_safe_data("x", current, 0))

        def get_start_at(start, end):
            s_x = start["x"]
            s_y = start["y"]
            e_x = end["x"]
            e_y = end["y"]
            x = width
            if s_x < e_x:
                x = width
                y = height / 2
            elif s_x == e_x:
                if s_y < e_y:
                    x = width / 2
                    y = height
                else:
                    x = width / 2
                    y = 0
            else:
                x = 0
                y = height / 2

            return [x, y]

        def handler_target_link(key, parent=None):
            links = []
            current = get_node_data(key)
            next = get_safe_data(self.get_next_name(), current)
            if not next:
                return links

            fail = get_safe_data(self.get_fail_name(), current)

            def get_link_data(current_key, next_key, current_node, n_node, node_type="next"):
                link = {
                    'id': current_key + "_" + next_key,
                    'startId': current_key,
                    'endId': next_key,
                    'startAt': get_start_at(current_node, n_node),
                    'endAt': get_start_at(n_node, current_node),
                    'meta': {
                        "desc": node_type
                    }
                }
                return link

            if isinstance(next, str):
                next_node = get_node_data(next)
                links.append(get_link_data(key, next, current, next_node))
            else:
                for next_child in next:

                    next_child_node = get_node_data(next_child)
                    links.append(get_link_data(key, next_child, current, next_child_node))
            if fail:
                fail_node = get_node_data(fail)
                # 如果是指向正常节点
                fail_node_type = get_safe_data(self.get_type_name(), fail_node)
                if fail_node_type != self.get_end_name():
                    links.append(get_link_data(key, fail, current, fail_node, node_type="fail"))

            # 处理正常流程
            if isinstance(next, str):
                links += handler_target_link(next, get_safe_data(self.get_key_name(), current))
            elif isinstance(next, list):

                for index, child in enumerate(next):
                    links += handler_target_link(child, get_safe_data(self.get_key_name(), current))

            # 处理失败流程
            if isinstance(fail, str):
                links += handler_target_link(fail, get_safe_data(self.get_key_name(), current))

            return links

        # 从根节点开始遍历
        handler_target_node(self.get_start_name(), None)
        links = handler_target_link(self.get_start_name(), None)
        target_list = []
        for key in parse_node_dict:
            target = get_target_node(parse_node_dict[key])
            target_list.append(target)
        result = {
            "nodes": target_list,
            "links": links
        }
        return self.success(result)
