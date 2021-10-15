# -*- coding: utf-8 -*-
"""
@Time: 2021/8/25 9:53
@Author: zzhang zzhang@cenboomh.com
@File: file_response.py
@desc:
"""
from collect.service_imp.result_handlers.result_handler import ResultHandler
from collect.utils.collect_utils import get_safe_data, Result


class FileResponse(ResultHandler):
    fr_const = {
        "filename_name": "filename"
    }

    def get_filename_name(self):
        return self.fr_const["filename_name"]

    def handler(self, result, config, template):
        params = get_safe_data(self.get_params_name(), config)
        if not params:
            return self.fail("文件处理器没有找到 {params} 节点".format(params=self.get_params_name()))

        path_name = get_safe_data(self.get_path_name(), params)
        if not path_name:
            return self.fail("文件处理器" + self.get_path_name() + " 节点")
        filename = get_safe_data(self.get_filename_name(), params)
        if not filename:
            return self.fail("文件处理器" + self.get_filename_name() + " 节点")
        params_result = self.get_params_result(template)
        path = get_safe_data(path_name, params_result)

        if not path:
            return self.fail("沒有找到参数" + path_name)
        import os
        if not os.path.exists(path):
            return self.fail(path + "文件不存在！！！")
        from collect.service_imp.common.filters.template_tool import TemplateTool
        tool = TemplateTool(op_user=self.op_user)

        def get_render_data(name):
            if name in params_result:
                return params_result[name]
            else:
                return tool.render(name, params_result)

        path = get_render_data(path)
        filename = get_render_data(filename)
        file = Result.file_response(path, filename=filename)
        return self.success(file)
