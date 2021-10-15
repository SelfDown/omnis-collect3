# -*- coding: utf-8 -*-
"""
@Time: 2021/6/18 15:17
@Author: zzhang zzhang@cenboomh.com
@File: Data2ExcelRule
@desc:
"""
import xlwt
from django.http import HttpResponse

from collect.collect_service import CollectService
from collect.utils.collect_utils import get_safe_data


class Data2ExcelRule(CollectService):
    def __init__(self):
        """

        """

    def get_result_obj(self, result, template):
        """
        将数据结果生成为，excel
        :param result:
        :param template:
        :return:
        """
        # excel_template_path = template["excel_template_path"]
        excel_out_path = template["excel_out_path"]
        file_name = template["file_name"]
        excel = template["excel"]
        from xlutils import copy
        import xlrd
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
        for sheet_index in excel:
            excel_template = excel[sheet_index]
            sheet = workbook.add_sheet("Sheet" + str(sheet_index))
            start_row = get_safe_data("start_row", excel_template, 2)
            title_row = get_safe_data("title_row", excel_template, 0)
            title = get_safe_data("title", excel_template, "盛博汇")
            name_row = get_safe_data("name_row", excel_template, 1)
            fields = excel_template["fields"]
            title_style = get_safe_data("title_style", excel_template,
                                        'font:color white ,height 240;pattern: pattern solid, fore_colour light_blue;')
            name_style = get_safe_data("name_style", excel_template,
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
            sheet.set_vert_split_pos(get_safe_data("frozen_col", excel_template, 1))
            for col, field in enumerate(fields):
                field_name = field['value']
                name = field['name']
                col_info = sheet.col(col)
                width = get_safe_data("width", field, 80)
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
        import os
        excel_dir = os.path.dirname(excel_out_path)
        if not os.path.exists(excel_dir):
            os.makedirs(excel_dir)

        workbook.save(excel_out_path)
        data = {"path": excel_out_path, "file_name": file_name}
        return self.success(data)
