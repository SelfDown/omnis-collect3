# -*- coding: utf-8 -*-
"""
@Time: 2021/7/21 13:52
@Author: zzhang zzhang@cenboomh.com
@File: base_rule.py
@desc:
"""
import json

from collect.collect_service import CollectService
from collect.service_imp.common.filters.template_tool import TemplateTool
from collect.utils.collect_utils import get_safe_data, DateEncoder


class BaseRule(CollectService):
    def get_path_class_result(self, path, class_name, params, config_params, template):
        import importlib
        check_factory = importlib.import_module(path)
        check_obj = getattr(check_factory, class_name)(op_user=self.op_user)
        success, data, msg = check_obj.handler(params, config_params, template)
        if not success:
            return self.fail(msg)
        return self.success(data, msg=msg)



    def has_template_str(self, node, field="template"):
        switch = get_safe_data(self.get_switch_name(), node)
        if switch and isinstance(switch, list):
            for item in switch:
                templ = get_safe_data(self.get_template_name(), item)
                if not templ:
                    return False
            return True
        if field not in node:
            return False

        template_str = node[field]
        return self.is_template_text(template_str)


    def handler_node(self, key, node, params, config_params, template=None, check=False):
        """
        处理顺序，自定义方法> service> template
        处理模板规则节点
        :return:
        """
        # 自定义方法
        path = get_safe_data(self.get_path_name(), node)
        class_name = get_safe_data(self.get_class_name(), node)
        # 配置服务
        service = get_safe_data(self.get_service_name(), node)
        enable = get_safe_data(self.get_enable_name(), node)
        template_tool = TemplateTool(op_user=self.op_user)
        # 检查是否禁用了，如果禁用了直接返回
        if enable:
            enable_value = template_tool.render(enable, params)
            if enable_value == self.get_false_value():
                return self.success(params)
        service_result = None
        config_param = config_params[key]
        if path and class_name:
            # 自定义检查
            path_class_result = self.get_path_class_result(path, class_name, params, config_params, template)
            return path_class_result
        if service:
            # template_tool = TemplateTool(op_user=self.op_user)
            # for key in service:
            #     value_template = service[key]
            #     if value_template in params:
            #         service[key] = params[value_template]
            #     else:
            #         value = template_tool.render(value_template, params, config_params, template)
            #         service[key] = value
            service_data = self.get_node_service(node=node, params=params, template=template, append_param=False)
            if not service_data:
                return service_data
            service = self.get_data(service_data)
            service_result = self.get_service_result(service, self.template)
            params[self.get_service_result_name()] = self.get_data(service_result)
            # 没有配置模板，或者结果是错误
            if not self.is_success(service_result):
                return service_result

        # 如果没有模板就返回
        if not self.has_template_str(node):
            # 有服务结果，返回服务结果
            if service_result:
                return self.success(service_result)
            else:
                self.log(json.dumps(node))
                self.log("没有找到"+self.get_template_name()+"")
                return self.success(params)
        # 普通模板
        # template_result = self.get_template_result(template_str, params, config_params, template)
        template_result = self.get_node_template_result(node, params, self.get_template_name(), config_params, template)
        if self.is_success(template_result):
            template_result_data = self.get_data(template_result)

            if check and template_result_data == 'False':
                err_msg = get_safe_data(self.get_err_msg_name(), node)
                if not err_msg:
                    node_info = json.dumps(node,cls=DateEncoder)
                    return self.fail("检查结果失败,没有配置" + self.get_err_msg_name()+":"+node_info)
                template_tool = TemplateTool(op_user=self.op_user)
                msg = template_tool.render(err_msg, params, config_params, template)
                return self.fail(msg)

        return template_result
