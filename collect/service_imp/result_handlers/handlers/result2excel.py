# -*- coding: utf-8 -*-
"""
@Time: 2021/8/25 17:45
@Author: zzhang zzhang@cenboomh.com
@File: result2excel.py
@desc:
"""

from collect.service_imp.result_handlers.result_handler import ResultHandler
from collect.utils.collect_utils import get_safe_data


class Result2Excel(ResultHandler):
    re_const = {
        # "file_name_name": "file_name",
        "excel_path_name": "excel_path",
        "excel_name": "excel",
        "sheet_name": "Sheet",
        "start_row_name": "start_row",
        "title_row_name": "title_row",
        "title_name": "title",
        "name_row_name": "name_row",
        "fields_name": "fields",
        "title_style_name": "title_style",
        "name_style_name": "name_style",
        "frozen_col_name": "frozen_col",
        "width_name": "width",
    }

    def get_width_name(self):
        return self.re_const["width_name"]

    def get_frozen_col_name(self):
        return self.re_const["frozen_col_name"]

    def get_name_style_name(self):
        return self.re_const["name_style_name"]

    def get_title_style_name(self):
        return self.re_const["title_style_name"]

    def get_fields_name(self):
        return self.re_const["fields_name"]

    def get_name_row_name(self):
        return self.re_const["name_row_name"]

    def get_title_name(self):
        return self.re_const["title_name"]

    def get_title_row_name(self):
        return self.re_const["title_row_name"]

    def get_start_row_name(self):
        return self.re_const["start_row_name"]

    def get_sheet_name(self):
        return self.re_const["sheet_name"]

    def get_excel_name(self):
        return self.re_const["excel_name"]

    def get_excel_path_name(self):
        return self.re_const["excel_path_name"]

    # def get_file_name_name(self):
    #     return self.re_const["file_name_name"]

    def handler(self, result, config, template):
        """
        将数据结果生成为，excel
        :param result:
        :param template:
        :return:
        """
        params = get_safe_data(self.get_params_name(), config)
        if not params:
            return self.fail("Excel处理器没有找到 {params} 节点".format(params=self.get_params_name()))
        # file_name = get_safe_data(self.get_file_name_name(), params)
        # if not file_name:
        #     return self.fail("Excel处理器params 节点没有找到{field}".format(field=self.get_file_name_name()))

        excel_path_name = get_safe_data(self.get_excel_path_name(), params)
        if not excel_path_name:
            return self.fail("Excel处理器params 节点没有找到{field}".format(field=self.get_excel_path_name()))
        excel = get_safe_data(self.get_excel_name(), template)
        if not excel:
            return self.fail("模板中没有找到{field}".format(field=self.get_excel_name()))
        import xlwt
        # book = xlrd.open_workbook(excel_template_path, formatting_info=True)
        workbook = xlwt.Workbook(encoding='utf-8')  # 新建工作簿
        # 单元格式纯文本
        style = xlwt.XFStyle()
        style.alignment.wrap = 1
        style.num_format_str = '@'
        from xlwt import Font
        fnt = Font()  # 创建一个文本格式，包括字体、字号和颜色样式特性
        fnt.name = u'微软雅黑'  # 设置其字体为微软雅黑
        style.font = fnt  # 将赋值好的模式参数导入Style
        from collect.service_imp.common.filters.template_tool import TemplateTool
        tool = TemplateTool(op_user=self.op_user)
        params_result = self.get_params_result(template)

        def get_render_data(name):
            if name in params_result:
                return params_result[name]
            else:
                return tool.render(name, params_result)

        for sheet_index in excel:
            excel_template = excel[sheet_index]
            sheet = workbook.add_sheet(self.get_sheet_name() + str(sheet_index))
            start_row = get_safe_data(self.get_start_row_name(), excel_template, 2)
            title_row = get_safe_data(self.get_title_row_name(), excel_template, 0)
            title = get_safe_data(self.get_title_name(), excel_template, "盛博汇")
            name_row = get_safe_data(self.get_name_name(), excel_template, 1)
            fields = excel_template[self.get_fields_name()]
            fields = [field_node for field_node in fields if self.is_enable(params_result, field_node)]
            title_style = get_safe_data(self.get_title_style_name(), excel_template,
                                        'font:color white ,height 240;pattern: pattern solid, fore_colour light_blue;')
            name_style = get_safe_data(self.get_name_style_name(), excel_template,
                                       'font:color white ;pattern: pattern solid, fore_colour ocean_blue;')
            tall_style = xlwt.easyxf(title_style)
            name_style = xlwt.easyxf(name_style)
            # 设置标题
            if not isinstance(title, unicode):
                title = unicode(str(title))
            sheet.write_merge(title_row, title_row, 0, len(fields) - 1, title, tall_style)
            sheet.row(0).height_mismatch = True
            sheet.row(0).height = 20 * 25  # 20为基准数，40意为40磅
            # 冻结
            sheet.set_panes_frozen('1')
            sheet.set_horz_split_pos(name_row + 1)
            sheet.set_vert_split_pos(get_safe_data(self.get_frozen_col_name(), excel_template, 1))

            for col, field in enumerate(fields):
                field_name = field[self.get_value_name()]
                name = field[self.get_name_name()]
                col_info = sheet.col(col)
                width = get_safe_data(self.get_width_name(), field, 80)
                try:
                    col_info.width = width * 50
                except Exception as e:
                    pass

                # 写列信息
                if not isinstance(name, unicode):
                    name = unicode(str(name))
                sheet.write(name_row, col, name, name_style)
                for row, data in enumerate(result):
                    value = data[field_name]
                    if value is None:
                        value = ""
                    # 写内容
                    if not isinstance(value, unicode):
                        value = unicode(str(value))
                    sheet.write(row + start_row, col, value, style)
            for row_plus in range(400):
                for col, field in enumerate(fields):
                    sheet.write(row_plus + start_row + len(result), col, "", style)

        excel_path = get_render_data(excel_path_name)
        import os
        excel_dir = os.path.dirname(excel_path)
        if not os.path.exists(excel_dir):
            os.makedirs(excel_dir)

        workbook.save(excel_path)
        return self.success(result)
