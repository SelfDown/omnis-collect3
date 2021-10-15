# -*- coding: utf-8 -*-
"""
@Time: 2021/8/24 15:56
@Author: zzhang zzhang@cenboomh.com
@File: server_copy.py
@desc:
"""
from collect.service_imp.flow.omnis_ssh import OmnisSSHService
from collect.utils.collect_utils import get_safe_data


class ServerArchive(OmnisSSHService):
    def handler(self, params, config, template):
        from_path = get_safe_data(self.get_from_path_name(), config)
        if not from_path:
            return self.fail("配置中沒有找到来源文件位置")
        from collect.service_imp.common.filters.template_tool import TemplateTool
        tool = TemplateTool(op_user=self.op_user)
        if self.is_template_text(from_path):
            from_path = tool.render(from_path, params)
        import os
        if not os.path.exists(from_path):
            return self.fail(from_path + "文件不存在")

        file_name = os.path.basename(from_path)
        import shutil
        try:
            dest = shutil.make_archive(from_path, "zip", from_path)
        except Exception as e:
            return self.fail(str(e))
        return self.success(dest)
        # if not os.path.exists(to_path):
        #     dir = os.path.dirname(to_path)
        #
