# -*- coding: utf-8 -*-
"""
@Time: 2021/8/17 10:15
@Author: zzhang zzhang@cenboomh.com
@File: ssh_copy.py
@desc:
"""
from collect.service_imp.flow.omnis_ssh import OmnisSSHService
from collect.utils.collect_utils import get_safe_data




class GenTemplate(OmnisSSHService):

    def handler(self, params, config, template):
        from_path = get_safe_data(self.get_from_path_name(), config)
        if not from_path:
            return self.fail("配置中沒有找到来源文件位置")
        to_path = get_safe_data(self.get_to_path_name(), config)
        if not to_path:
            return self.fail("配置中沒有找到目标文件位置")
        from collect.service_imp.common.filters.template_tool import TemplateTool
        tool = TemplateTool(op_user=self.op_user)
        if self.is_template_text(from_path):
            from_path = tool.render(from_path, params)
        import os
        if not os.path.exists(from_path):
            return self.fail(from_path + "文件不存在")

        if os.path.isdir(from_path):
            return self.fail(from_path + "是个文件夹，不支持")

        if self.is_template_text(to_path):
            to_path = tool.render(to_path, params)

        to_dir = os.path.dirname(to_path)
        if not os.path.exists(to_dir):
            os.makedirs(to_dir)
        with open(from_path) as f:
            templ = f.read()
        content = tool.render(templ, params)
        import re
        content_unix = re.sub(r'\r\n', r'\n', content)
        with open(to_path,  mode='wb') as f:
            f.write(content_unix)
        return self.success(to_path)
