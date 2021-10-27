# -*- coding: utf-8 -*-
"""
@Time: 2021/8/17 10:15
@Author: zzhang zzhang@cenboomh.com
@File: ssh_copy.py
@desc:
"""
from collect.service_imp.flow.omnis_ssh import OmnisSSHService
from collect.utils.collect_utils import get_safe_data


class SCPCopy(OmnisSSHService):
    def remote_file_exists(self, ssh, dest_path, template):
        result = self.execute_base_shell_with_log("ls " + dest_path, ssh, template=template)
        result_data = self.get_data(result)
        if self.has_error(result_data):
            return False
        else:
            return True

    def mkdirs(self, ssh, dest_path, template):
        result = self.execute_base_shell_with_log("mkdir -p  " + dest_path, ssh, template=template)
        result_data = self.get_data(result)
        if self.has_error(result_data):
            return False, result_data
        else:
            return True, ""

    def handler(self, params, config, template):
        from_path = get_safe_data(self.get_from_path_name(), config)
        if not from_path:
            return self.fail("配置中沒有找到来源文件位置")
        to_path = get_safe_data(self.get_to_path_name(), config)
        if not to_path:
            return self.fail("配置中沒有找到目标文件位置")
        from collect.service_imp.common.filters.template_tool import TemplateTool
        tool = TemplateTool(op_user=self.op_user)
        # if self.is_template_text(from_path):
        #     from_path = tool.render(from_path, params)
        from_path = self.get_render_data(from_path, params, tool=tool)
        import os
        if not os.path.exists(from_path):
            return self.fail(from_path + "文件不存在")

        if os.path.isdir(from_path):
            return self.fail(from_path + "是个文件夹，不支持")

        # if self.is_template_text(to_path):
        #     to_path = tool.render(to_path, params)
        to_path = self.get_render_data(to_path, params, tool=tool)
        scp_result = self.get_scp_client(template)
        if not self.is_success(scp_result):
            return scp_result
        scp = self.get_data(scp_result)
        # dest_path = None
        # 如果目标文件“.”有后缀，表示是文件
        if "." in os.path.basename(to_path):
            dest_path = os.path.dirname(to_path)
            dest_file = os.path.basename(to_path)
        else:  # 如果目标文件没有后缀，则表示是个目录
            dest_path = to_path
            dest_file = os.path.basename(from_path)

        if not dest_file:
            return self.fail("源文件不存在")
        ssh = self.get_ssh_data(template)
        if not self.remote_file_exists(ssh, dest_path, template):
            status, result_data = self.mkdirs(ssh, dest_path, template)
            if not status:
                return self.fail(result_data)
        try:
            if not dest_path.endswith("/"):
                dest_path += "/"
            dest = dest_path + dest_file
            scp.put(from_path, dest)
        except Exception as e:
            msg = str(e)
            p = {"path": dest_path}
            msg = self.get_error_msg(msg, template, p)
            return self.fail(msg)

        return self.success(dest)
