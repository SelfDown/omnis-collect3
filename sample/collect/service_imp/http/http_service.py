# -*- coding: utf-8 -*-
"""
@Time: 2021/7/14 16:32
@Author: zzhang zzhang@cenboomh.com
@File: ModelUpdate.py
@desc:
"""
from collect.collect_service import CollectService
from collect.utils.collect_utils import get_safe_data


class HttpService(CollectService):
    data_json_dict = {}
    HConst = {
        "data_json_name": "data_json",
        "success_name": "success",
    }

    def __init__(self, op_user):
        CollectService.__init__(self, op_user)
        self.api = HttpApi(op_user)
        pass

    def get_success_name(self):
        return self.HConst["success_name"]

    def get_data_json_name(self):
        return self.HConst["data_json_name"]

    @staticmethod
    def get_json_content(path):
        return get_safe_data(path, HttpService.data_json_dict)

    @staticmethod
    def set_json_content(path, data_json_content):
        HttpService.data_json_dict[path] = data_json_content

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

    def get_http_param(self, data_json_templ, params_result):
        from collect.service_imp.common.filters.template_tool import TemplateTool
        tool = TemplateTool(op_user=self.op_user)
        data_json = tool.render(data_json_templ, params_result)
        try:
            import json
            data_json = json.loads(data_json)
            return self.success(data_json)
        except Exception as e:
            self.log(data_json, "error")
            return self.fail(str(e) + " JSON格式有误，请检查配置")

    def result(self, params=None):
        params_result = self.get_params_result()

        success_temp = get_safe_data(self.get_success_name(), self.template)
        if not success_temp:
            return self.fail("HTTP请求模块没有配置" + self.get_success_name())
        data_json_result = self.get_data_json(params_result)
        if not self.is_success(data_json_result):
            return data_json_result
        data_json_templ = self.get_data(data_json_result)
        data_json_result = self.get_http_param(data_json_templ, params_result)
        if not self.is_success(data_json_result):
            return data_json_result
        data_json = self.get_data(data_json_result)
        result = self.api.send(data_json)
        if not self.is_success(result):
            return result
        result_data = self.get_data(result)
        if isinstance(result_data, dict):
            from collect.service_imp.common.filters.template_tool import TemplateTool
            tool = TemplateTool(op_user=self.op_user)
            val = tool.render(success_temp, result_data)
            if val == self.get_false_value():
                err_msg = get_safe_data(self.get_err_msg_name(), self.template)
                if not err_msg:
                    return self.fail("HTTP 模块没有配置" + self.get_err_msg_name())
                message = self.get_render_data(err_msg, result_data, tool)
                return self.fail(message)
        params_result["http_send"] = data_json
        return self.success(data=result_data, msg="发送成功")


class HttpApi(CollectService):

    def __init__(self, op_user):
        """
         调用监控模块
        """
        CollectService.__init__(self, op_user)

    def send(self, data):
        import requests
        import json
        try:
            r = requests.request(**data)
        except Exception as e:
            self.log("监控请求发送失败", level="error")
            return self.fail(msg=str(e))
        if r.status_code != 200:
            self.log(r.text)
        try:
            result_data = json.loads(r.text)
        except Exception as e:
            self.log("数据返回错误：" + str(e) + "\n\n" + r.text)
            return self.fail(msg="数据返回格式错误")

        return self.success(result_data)
