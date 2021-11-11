# -*- coding: utf-8 -*-
"""
@Time: 2021/8/16 16:23
@Author: zzhang zzhang@cenboomh.com
@File: omnis_flow.py
@desc:
"""
from collect.collect_service import CollectService
from collect.utils.collect_utils import get_safe_data


class ServiceOmnisFlowService(CollectService):
    flow_const = {
        "services_name": "services",
        "name_name": "name",
        "start_name": "start",
        "end_name": "end",
        "next_name": "next",
        "fail_name": "fail",
        "ignore_error_name": "ignore_error",
    }

    # 最大服务运行次数
    max = 20

    def __init__(self, op_user):
        CollectService.__init__(self, op_user=op_user)
        self.flow_config = None
        self.flow_name = None
        self.must_node_names = []

    def get_ignore_error_name(self):
        return self.flow_const["ignore_error_name"]

    def set_must_node_names(self, names):
        self.must_node_names = names

    def get_must_node_names(self):
        return self.must_node_names

    def get_flow_name(self):
        return self.flow_name

    def set_flow_name(self, flow_name):
        self.flow_name = flow_name

    def get_flow(self):
        return self.flow_config

    def set_flow(self, flow_config):
        self.flow_config = flow_config

    def get_services(self):
        flow = self.get_flow()
        if not flow:
            return
        return get_safe_data(self.get_services_name(), flow)

    def get_services_name(self):
        return self.flow_const["services_name"]

    def get_end_name(self):
        return self.flow_const["end_name"]

    def get_next_name(self):
        return self.flow_const["next_name"]

    def get_start_name(self):
        return self.flow_const["start_name"]

    def get_start_node(self, service_dict):
        return get_safe_data(self.get_start_name(), service_dict)

    def get_end_node(self, service_dict):
        return get_safe_data(self.get_end_name(), service_dict)

    def get_service_dict(self):
        services = self.get_services()
        d = {}
        for index, item in enumerate(services):
            key = get_safe_data(self.get_key_name(), item)

            def err_info(name):
                return "第【{index}】服务节点,【{key}】没有【{name}】 属性".format(index=str(index + 1), key=str(key), name=str(name))

            if not key:
                return self.fail(err_info(self.get_key_name()))
            t = get_safe_data(self.get_type_name(), item)
            if not t:
                return self.fail(err_info(self.get_type_name()))
            # 除结尾节点，都要配置next 标签
            if t not in (self.get_end_name()):
                next = get_safe_data(self.get_next_name(), item)
                if not next:
                    return self.fail(err_info(self.get_next_name()))
            if t not in (self.get_start_name(), self.get_end_name()):
                has = False
                names = self.get_must_node_names()
                for name in names:
                    if name in item:
                        has = True
                if not has and len(names) > 0:
                    err_node_names = ",".join(names)
                    return self.fail(err_info(err_node_names))

            name = get_safe_data(self.get_name_name(), item)
            if not name:
                return self.fail(err_info(self.get_name_name()))
            if key in d:
                return self.fail(
                    self.get_template_service_name() + "第【" + str(index + 1) + "】服务节点,流程已经存在【" + key + "】节点")
            d[key] = item
        start = self.get_start_node(d)
        if not start:
            return self.fail("没有找到初始节点")
        end = self.get_end_node(d)
        if not end:
            return self.fail("没有找到结束节点")
        return self.success(d)

    def get_fail_name(self):
        return self.flow_const["fail_name"]

    def get_next_node(self, node, service_dict, node_result=None):
        current_name = get_safe_data(self.get_name_name(), node)
        params = self.get_params_result()
        import json
        if self.can_log():
            self.log(json.dumps(node_result))
        if not node_result or self.is_success(node_result): # 运行正常
            field = self.get_next_name()
            # 获取下个节点
            node_result = self.get_node_template_result(node, params, field=field, template=self.get_template())
            if self.can_log():
                self.log(json.dumps(node_result))
        else: # 运行错误
            fail = get_safe_data(self.get_fail_name(),node)
            if not fail:
                self.log("流程结果返回错误，但是" + current_name + "没有配置" + self.get_fail_name() )
            node_result = self.get_template_result(fail, params,template=self.get_template())
        next = self.get_data(node_result)
        next_node = get_safe_data(next, service_dict)
        if not next_node:
            self.log("流程结果返回错误，但是" + current_name + "没有找到" + next+"节点")
            return
        return get_safe_data(next, service_dict)
        # current_name = get_safe_data(self.get_name_name(), node)
        # if not node_result or self.is_success(node_result):
        #     next = get_safe_data(self.get_next_name(), node)
        # else:
        #     next = get_safe_data(self.get_fail_name(), node)
        #     if not next:
        #         self.log("流程结果返回错误，但是" + current_name + "没有配置" + self.get_fail_name())
        #         return
        #
        # if not next in service_dict and self.is_template_text(next):
        #     # from collect.service_imp.common.filters.template_tool import TemplateTool
        #     # template_tool = TemplateTool(op_user=self.op_user)
        #     params = self.get_params_result()
        #     node_result = self.get_node_template_result(node, params,field="next", template=self.get_template())
        #     if not self.is_success(node_result):
        #         return node_result
        #     next = self.get_data(node_result)
        #     # try:
        #     #     next = template_tool.render(next, params)
        #     # except Exception as e:
        #     #     self.log(current_name + "模板渲染获取下个节点失败" + str(e))
        #     #     return



    def flow(self, handler_node):
        services = self.get_services()
        if not services:
            return self.fail(msg=self.get_flow_name() + "节点,没有找到" + self.get_services_name() + "节点，请检查配置")

        service_dict_result = self.get_service_dict()
        if not self.is_success(service_dict_result):
            if self.can_log():
                self.log(self.get_msg(service_dict_result), level="error")
            return service_dict_result

        service_dict = self.get_data(service_dict_result)

        start = self.get_start_node(service_dict)
        current = self.get_next_node(start, service_dict)
        end = self.get_end_node(service_dict)
        count = 1
        params_result = self.get_params_result()

        first_err_msg = ""
        first_err = False
        while True:
            if not current:
                return self.fail(msg=self.get_template_service_name() + "运行到第【" + str(count) + "】 个节点，找不到下个节点了")
            if current == end:
                break
            current_name = get_safe_data(self.get_name_name(), current)
            if self.can_log():
                msg = "【" + self.get_template_service_name() + "】开始运行第 " + str(count) + " 节点【" + current_name + "】"
                self.log(msg)

            node_result = handler_node(current)
            nodes = self.get_data(node_result)
            if self.can_log() and nodes and isinstance(nodes,list):
                for n_item in nodes:
                    if isinstance(n_item, dict) and "success" in n_item and not self.is_success(n_item):
                        self.log(n_item)

            ignore_error = get_safe_data(self.get_ignore_error_name(), current)
            if ignore_error or ignore_error == self.get_true_value():
                if not self.is_success(node_result) and self.can_log():
                    msg = "忽略错误：运行第 " + str(count) + " 节点【" + current_name + "】失败" + self.get_msg(node_result)
                    self.log(msg, level="error")
                node_result["success"] = True
            if not self.is_success(node_result):
                if self.can_log():
                    msg = self.get_template_service_name() + "运行第 " + str(
                        count) + " 节点【" + current_name + "】失败" + self.get_msg(node_result)
                    self.log(msg)

                if first_err:
                    msg = self.get_template_service_name() + "已经得到2次错误返回结果。请检查流程节点配置【" + current_name + "】运行错误：" + msg + "。"
                    return self.fail(msg)
                msg = self.get_msg(node_result)
                first_err = True
                first_err_msg = msg

            # 保存数据
            save_field = get_safe_data(self.get_save_field_name(), current)
            if save_field:
                params_result[save_field] = self.get_data(node_result)
            # 流转到下个节点
            current = self.get_next_node(current, service_dict, node_result)
            count += 1
            if count >= self.max:
                return self.fail(msg="服务运行次数已经超过最大限制：" + str(self.max))
        if first_err:
            return self.fail(first_err_msg)
        result = {}
        return self.success(result)

    def handler_app(self, node, config, result=None):
        for key in config:
            if key in node:
                rule = config[key]
                config_params = node[key]
                params = self.get_params_result()
                import importlib
                path = rule[self.get_path_name()]
                class_name = rule[self.get_class_name()]
                collect_factory = importlib.import_module(path)
                rule_obj = getattr(collect_factory, class_name)(op_user=self.op_user)
                result = rule_obj.handler(params, config_params, template=self.template)
                if not self.is_success(result):
                    return result
                result = self.get_data(result)
                break
        return self.success(result)
