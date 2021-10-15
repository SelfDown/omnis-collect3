# -*- coding: utf-8 -*-
"""
@Time: 2021/7/14 16:32
@Author: zzhang zzhang@cenboomh.com
@File: ModelUpdate.py
@desc:
"""
from collect.collect_service import CollectService
from collect.utils.collect_utils import get_safe_data


class SessionService(CollectService):
    data_json_dict = {}
    SSConst = {
        "session_name": "session",
        "add_key_name": "add_key",
        "remove_key_name": "remove_key"
    }

    def __init__(self, op_user):
        CollectService.__init__(self, op_user)

        pass

    def get_session_name(self):
        return self.SSConst["session_name"]

    def add_key_name(self):
        return self.SSConst["add_key_name"]

    def remove_key_name(self):
        return self.SSConst["remove_key_name"]

    def get_session_config(self):
        return get_safe_data(self.get_session_name(), self.template)

    def result(self, params=None):
        session = self.get_session()
        session_config = self.get_session_config()
        params_result = self.get_params_result()
        tool = self.get_render_tool()
        for config in session_config:
            key = get_safe_data(self.get_key_name(), config)
            name = get_safe_data(self.get_name_name(), config)
            if key == self.add_key_name():
                templ = get_safe_data(self.get_template_name(), config)
                value = self.get_render_data(templ, params_result, tool)
                session[name] = value
            elif key == self.remove_key_name():
                if name in session:
                    del session[name]

        return self.success(data={}, msg="操作成功")
