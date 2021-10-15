# -*- coding: utf-8 -*-
"""
@Time: 2021/9/2 14:54
@Author: zzhang zzhang@cenboomh.com
@File: dir_tree.py
@desc:
"""
from collect.service_imp.flow.omnis_ssh import OmnisSSHService
from collect.utils.collect_utils import get_safe_data


class FileContent(OmnisSSHService):
    fc_const = {
        "file_name": "file",

    }

    def get_file_name(self):
        return self.fc_const["file_name"]

    def handler(self, params, config, template):
        file_name = get_safe_data(self.get_file_name(), config)
        if not file_name:
            return self.fail("没有找到" + self.get_file_name() + "属性")
        import os
        from collect.service_imp.common.filters.template_tool import TemplateTool
        tool = TemplateTool(op_user=self.op_user)
        params_result = self.get_params_result(template)

        file = self.get_render_data(file_name, params_result, tool)
        if not os.path.exists(file):
            return self.fail(file + "配置的文件路径不存在")

        with open(file) as f:
            content = f.read()
        return self.success(content)
