# -*- coding: utf-8 -*-
"""
@Time: 2021/9/2 14:54
@Author: zzhang zzhang@cenboomh.com
@File: dir_tree.py
@desc:
"""
from collect.service_imp.flow.omnis_ssh import OmnisSSHService
from collect.utils.collect_utils import get_safe_data, get_uuid


class DirTree(OmnisSSHService):
    dt_const = {
        "file_name": "file",
        "dir_name": "dir"
    }

    def get_file_name(self):
        return self.dt_const["file_name"]

    def get_dir_name(self):
        return self.dt_const["dir_name"]

    def get_dir_tree(self, dir):
        import os
        dirs = os.listdir(dir)
        tree = []
        file_list = []
        for current in dirs:
            c = {
                "key": dir.replace("\\", "/") + "/" + current,
                "name": current
            }
            current_path = os.path.join(dir, current)
            if os.path.isdir(current_path):
                c["type"] = "folder"
                children = self.get_dir_tree(current_path)
                c["children"] = children
                c["iconSkin"] = "i-folder"
                tree.append(c)
            elif os.path.isfile(current_path):
                c["type"] = "file"
                if current_path.endswith(".yaml") or current_path.endswith(".yml"):
                    c["iconSkin"] = "i-yaml"
                elif current_path.endswith(".sql"):
                    c["iconSkin"] = "i-sql"
                elif current_path.endswith(".json"):
                    c["iconSkin"] = "i-json"
                file_list.append(c)
        tree += file_list

        return tree

    def handler(self, params, config, template):
        file_name = get_safe_data(self.get_file_name(), config)
        dir_path = None
        import os
        from collect.service_imp.common.filters.template_tool import TemplateTool
        tool = TemplateTool(op_user=self.op_user)
        params_result = self.get_params_result(template)
        if file_name:

            file = self.get_render_data(file_name, params_result, tool)
            if not os.path.exists(file):
                return self.fail(file + "配置的文件路径不存在")
            dir_path = os.path.dirname(file)
        if not dir_path:
            dir_name = get_safe_data(self.get_dir_name(), config)
            dir_path = self.get_render_data(dir_name, params_result, tool)
            if not dir_path:
                return self.fail("没有配置路径")
        dir_tree = self.get_dir_tree(dir_path)
        return self.success(dir_tree)
