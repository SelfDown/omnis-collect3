# -*- coding: utf-8 -*-
"""
@Time: 2021/7/14 16:32
@Author: zzhang zzhang@cenboomh.com
@File: ModelUpdate.py
@desc:
"""
import json

from collect.collect_service import CollectService
from collect.utils.collect_utils import get_safe_data


class EventService(CollectService):
    data_json_dict = {}
    ESConst = {
        "data_json_name": "data_json",
        "from_name": "from",
        "before_params_append_name": "before_params_append",
        "to_name": "to",
        "bulk_service_name": "bulk_service",
        "bulk_result_field_name": "bulk_result_field",
        "finish_service_name": "finish_service",
        "log_create_name": "log_create",
        "log_update_name": "log_update",
        "log_save_service_name": "log_save_service",
        "log_update_service_name": "log_update_service"

    }

    def __init__(self, op_user):
        CollectService.__init__(self, op_user)
        self.event_template = None
        self.to_services = None
        self.create_log_list = []
        self.update_log_list = []

    def get_log_create_name(self):
        return self.ESConst["log_create_name"]

    def get_log_save_service_name(self):
        return self.ESConst["log_save_service_name"]

    def get_log_update_service_name(self):
        return self.ESConst["log_update_service_name"]

    def get_log_update_name(self):
        return self.ESConst["log_update_name"]

    def get_finish_service_name(self):
        return self.ESConst["finish_service_name"]

    def get_bulk_result_field_name(self):
        return self.ESConst["bulk_result_field_name"]

    def set_to_services(self, to_services):
        self.to_services = to_services

    def get_to_services(self):
        return self.to_services

    def get_bulk_service_name(self):
        return self.ESConst["bulk_service_name"]

    def get_before_params_append_name(self):
        return self.ESConst["before_params_append_name"]

    def get_from_name(self):
        return self.ESConst["from_name"]

    def get_event_template(self):
        return self.event_template

    def set_event_template(self, event_template):
        self.event_template = event_template

    def get_data_json_name(self):
        return self.ESConst["data_json_name"]

    def get_to_name(self):
        return self.ESConst["to_name"]

    @staticmethod
    def get_json_content(path):
        return get_safe_data(path, EventService.data_json_dict)

    @staticmethod
    def set_json_content(path, data_json_content):
        EventService.data_json_dict[path] = data_json_content

    def get_data_json_config_path(self):
        data_json = get_safe_data(self.get_data_json_name(), self.template)

        config_dir = self.get_config_dir()
        config_file = config_dir + "/" + data_json
        return config_file

    def get_data_json(self, params):
        config_file_path = self.get_data_json_config_path()
        json_content = self.get_json_content(config_file_path)
        if json_content:
            return self.success(json_content)
        data_json = get_safe_data(self.get_data_json_name(), self.template)
        data_json_result = self.get_config_file(data_json, params)
        if self.is_success(data_json_result):
            data_json_content = self.get_data(data_json_result)
            self.set_json_content(config_file_path, data_json_content)
        return data_json_result

    def get_event_param(self, data_json_templ):
        from collect.service_imp.common.filters.template_tool import TemplateTool
        # tool = TemplateTool(op_user=self.op_user)
        # data_json = tool.render(data_json_templ, params_result)
        try:
            import json
            data_json = json.loads(data_json_templ)
            return self.success(data_json)
        except Exception as e:
            self.log(data_json_templ, "error")
            return self.fail(str(e) + " JSON格式有误，请检查配置")

    def event_check(self):
        from_services = get_safe_data(self.get_from_name(), self.get_event_template())
        if not from_services:
            return self.fail("没有配置来源服务")
        params_result = self.get_params_result()
        from_service = get_safe_data(self.get_from_service_name(), params_result)
        if from_service not in from_services:
            return self.fail("非法服务,请检查配置")
        return self.success([])

    def before_event(self):
        params_result = self.get_params_result()
        event_template = self.get_event_template()
        appends = get_safe_data(self.get_before_params_append_name(), event_template)
        if appends:
            # 添加一些变量
            tool = self.get_render_tool()
            for item in appends:
                field = get_safe_data(self.get_field_name(), item)
                temp = get_safe_data(self.get_template_name(), item)
                params_result[field] = self.get_render_data(temp, params_result, tool)

        to_services = get_safe_data(self.get_to_name(), event_template)
        if not to_services:
            return self.fail("没有找到目标服务")

        tool = self.get_render_tool()
        services = []
        # 拼接服务
        for index, to_service in enumerate(to_services):
            service = get_safe_data(self.get_service_name(), to_service)
            if not self.is_enable(to_service, params_result):
                continue
            if not service:
                return self.fail(" 第 " + str(index + 1) + "个服务没有配置 " + self.get_service_name())
            # 处理外部参数
            for field in to_service:
                temp = to_service[field]
                if self.is_template_text(temp):
                    to_service[field] = tool.render(temp, params_result)
            # 处理service
            self.get_node_service(to_service, params_result)
            # 添加日志
            service_item = get_safe_data(self.get_service_name(), to_service)
            self.add_create_log_data(service_item)
            services.append(service_item)
        if len(services) <= 0:
            return self.fail("没有找的事件执行服务")
        self.set_to_services(services)
        self.create_log_data()
        return self.success([])

    def get_template_log(self):

        log = get_safe_data(self.get_log_name(), self.get_event_template())
        import copy
        return copy.deepcopy(log)

    def can_log_data(self):
        """
         判断是否需要记录日志
        """
        log = self.get_template_log()
        if not log:
            return False
        else:
            return True

    def get_service_item_params(self, service_item=None, result=None, create_log_list=None, update_log_list=None):
        item = {
            "params": self.get_params_result()
        }
        if service_item:
            item["service_item"] = service_item
        if result:
            item["result"] = result
        if update_log_list:
            item["update_log_list"] = update_log_list

        if create_log_list:
            item["create_log_list"] = create_log_list
        return item

    def get_log_data(self, node_name, service_item=None, result=None, create_log_list=None, update_log_list=None):
        template_log = self.get_template_log()
        params = self.get_service_item_params(service_item=service_item, result=result, create_log_list=create_log_list,
                                              update_log_list=update_log_list)
        log = get_safe_data(node_name, template_log)
        service = {self.get_service_name(): log}
        create_item = self.get_node_service(service, params, append_param=False)
        if not self.is_success(create_item):
            self.log(self.get_msg(create_item), level="error")
            return False
        return self.get_data(create_item)

    def add_create_log_data(self, service_item):
        """
        添加日志记录
        """
        if not self.can_log_data():
            return False
        create_item = self.get_log_data(node_name=self.get_log_create_name(), service_item=service_item)
        if create_item:
            self.create_log_list.append(create_item)

    def create_log_data(self):
        """
        执行日志添加服务
        """
        if not self.can_log_data():
            return False
        create_log_service = self.get_log_data(node_name=self.get_log_save_service_name(),
                                               create_log_list=self.create_log_list)
        create_log_service_result = self.get_service_result(create_log_service)
        if not self.is_success(create_log_service_result):
            self.log(self.get_msg(create_log_service_result), level="error")

    def add_update_log_data(self, service_item, result):
        """
        添加更新日志
        """
        if not self.can_log_data():
            return False
        update_item = self.get_log_data(node_name=self.get_log_update_name(), service_item=service_item, result=result)
        if update_item:
            self.update_log_list.append(update_item)

    def update_log_data(self):
        """
        执行日志更新服务
        """
        if not self.can_log_data():
            return False
        update_log_service = self.get_log_data(node_name=self.get_log_update_service_name(),
                                               update_log_list=self.update_log_list)
        update_log_service_result = self.get_service_result(update_log_service)
        if not self.is_success(update_log_service_result):
            self.log(self.get_msg(update_log_service_result), level="error")

    def after_event(self):
        event_template = self.get_event_template()
        params_result = self.get_params_result()

        req = get_safe_data(self.get_finish_service_name(), event_template)
        if req:
            # 构造结束服务
            node = {
                self.get_service_name(): req
            }
            finish = self.get_node_service(node, params_result, append_param=False)
            finish = self.get_data(finish)
            if self.can_log():
                self.log(json.dumps(finish))
            # 执行结束服务
            finish_result = self.get_service_result(finish)
            if self.can_log():
                self.log(json.dumps(finish_result))
            if not self.is_success(finish_result):
                return finish_result

        return self.success([])

    def execute_event(self):
        event_template = self.get_event_template()
        params_result = self.get_params_result()
        to_services = self.get_to_services()
        params_result[self.get_to_name()] = to_services
        req = get_safe_data(self.get_bulk_service_name(), event_template)
        if not req:
            return self.fail("没有配置批量执行的服务")
        # 构造批量服务
        node = {
            self.get_service_name(): req
        }
        bulk = self.get_node_service(node, params_result, append_param=False)
        bulk = self.get_data(bulk)
        if self.can_log():
            self.log(json.dumps(bulk))
        # 批量执行服务
        bulk_result = self.get_service_result(bulk)
        if self.can_log():
            self.log(json.dumps(bulk_result))
        bulk_result_field = get_safe_data(self.get_bulk_result_field_name(), event_template)
        # 设置批量结果
        if not self.is_success(bulk_result):
            return bulk_result
        res = self.get_data(bulk_result)
        if bulk_result_field:
            params_result[bulk_result_field] = res
        del params_result[self.get_to_name()]
        # 设置单个结果
        for request, result in zip(get_safe_data(self.get_to_name(), event_template), res):
            save_field = get_safe_data(self.get_save_field_name(), request)
            params_result[save_field] = result
            self.add_update_log_data(get_safe_data(self.get_service_name(), request), result)
        # 构造结束服务
        self.update_log_data()
        return self.success([])

    def result(self, params=None):
        params_result = self.get_params_result()
        data_json_result = self.get_data_json(params_result)
        if not self.is_success(data_json_result):
            return data_json_result
        data_json_templ = self.get_data(data_json_result)
        data_json_result = self.get_event_param(data_json_templ)
        if not self.is_success(data_json_result):
            return data_json_result
        event_template = self.get_data(data_json_result)
        self.set_event_template(event_template)
        # 检查
        check_result = self.event_check()
        if not self.is_success(check_result):
            return check_result
        # 执行前
        before_result = self.before_event()
        if not self.is_success(before_result):
            return before_result
        # 执行中
        execute_result = self.execute_event()
        if not self.is_success(execute_result):
            return execute_result
        # 执行后
        after_result = self.after_event()
        if not self.is_success(after_result):
            return after_result
        return self.success(data={}, msg="发送成功")
