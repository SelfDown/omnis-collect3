# -*- coding: utf-8 -*-
"""
@Time: 2021/6/21 11:22
@Author: zzhang zzhang@cenboomh.com
@File: excel_service.py
@desc:
"""
from collect.collect_service import CollectService
from collect.utils.collect_utils import get_safe_data, Result


class ExcelService(CollectService):
    def __init__(self, op_user=None):

        CollectService.__init__(self,op_user=op_user)
        self.op_user = op_user

    def download(self, data):
        """
        下载excel
        :param data:
        :return:
        """
        service = get_safe_data("service", data)
        collect_service = CollectService(op_user=self.op_user)
        result = collect_service.make_service(service)

        if not collect_service.is_success(result):
            msg = collect_service.get_msg(result)
            return Result.fail_response(msg=msg)
        service_obj = collect_service.get_data(result)
        # 查询数据
        params = data
        return_result = service_obj.result(params)
        msg = collect_service.get_msg(return_result)
        if not service_obj.is_success(return_result):
            return Result.fail_response(msg=msg)
        data = service_obj.get_data(return_result)
        # 处理数据
        data = service_obj.filter_result_obj(data)

        if service_obj.is_file_result():
            data = service_obj.get_data(data)
            return Result.file_response(data["path"], data["file_name"])
        else:
            data = service_obj.get_data(data)
        return Result.success_response(data)

    def import_data(self, data):
        file = data.get("file", None)
        service = get_safe_data("service", data)
        collect_service = CollectService(op_user=self.op_user)
        # 获取实例对象
        result = collect_service.make_service(service)

        if not self.is_success(result):
            msg = collect_service.get_msg(result)
            return Result.fail_response(msg=msg)
        service_obj = collect_service.get_data(result)
        # 解析excel数据
        excel_result = self.get_excel_data(file, config=service_obj.get_excel_config())
        if not self.is_success(excel_result):
            msg = self.get_msg(excel_result)
            return Result.fail_response(msg=msg)
        # 删除文件
        del data["file"]
        params = data.copy()
        params[self.get_excel_result_name()] = self.get_data(excel_result)
        # 处理数据
        return_result = service_obj.result(params)
        msg = self.get_msg(return_result)
        if not self.is_success(return_result):
            return Result.fail_response(msg=msg)

        data = service_obj.get_data(return_result)
        return Result.success_response(data)

    def get_excel_data(self, file, config):
        """
        根据excel 转成 字典 记录
        :param file:

        :return:
        """
        with file as f:
            file_content = f.read()
        for sheet_index in config:
            import xlrd
            wb = xlrd.open_workbook(filename=None, file_contents=file_content)  # 关键点在于这里
            try:
                sheet_index = int(sheet_index)
                table = wb.sheets()[sheet_index]
            except Exception as e:
                return self.fail(msg="文件中找不到 {sheet_index}".format(sheet_index))

            nrows = table.nrows  # 行数
            ncole = table.ncols  # 列数
            sheet_config = config[sheet_index]
            data_list = []
            from_service_name = get_safe_data("from", sheet_config)
            # 字段=>序号
            from_sheet_config = None
            if from_service_name:
                collect_service = CollectService()
                arr = from_service_name.split(".")
                if len(arr) < 3:
                    return self.fail(
                        msg="配置有误，来源配置 {from_service_name} 配置有问题。示例hrm.user.0".format(
                            from_service_name=from_service_name))
                from_service = arr[0] + "." + arr[1]
                from_service = collect_service.make_service(from_service)
                from_service = self.get_data(from_service)
                if not from_service:
                    if not excel:
                        return self.fail(
                            msg="配置有误，来源配置 {from_service_name} 不存在 excel 节点".format(
                                from_service_name=from_service_name))

                excel = get_safe_data(self.get_excel_config_name(), from_service.template)
                if not excel:
                    return self.fail(
                        msg="配置有误，来源配置 {from_service_name} 服务不存在 ".format(from_service_name=from_service_name))
                try:
                    sheet_idx = int(arr[2])
                except Exception as e:
                    sheet_idx = 0
                if sheet_idx not in excel:
                    return self.fail(
                        msg="配置有误，来源配置 {from_service_name}  excel 节点中不存在 {sheet_idx} 标签".format(
                            from_service_name=from_service_name, sheet_idx=arr[2]))
                from_sheet_excel = get_safe_data(sheet_idx, excel)
                from_fields = get_safe_data("fields", from_sheet_excel)
                if not from_fields:
                    return self.fail(
                        msg="配置有误，来源配置 {from_service_name}  excel 节点中第 {sheet_idx} 标签，不存在fields 节点".format(
                            from_service_name=from_service_name, sheet_idx=arr[2]))
                from_sheet_config = {}
                for row_idx, field in enumerate(from_fields):
                    field_name = get_safe_data("value",field)
                    from_sheet_config[field_name] = row_idx

            for i in range(sheet_config["start_row"], nrows):
                rowValues = table.row_values(i)  # 一行的数据

                data_obj = {}
                for field in sheet_config["fields"]:
                    col_index = get_safe_data("col_index", field)
                    field_name = get_safe_data("value", field)
                    if not col_index and from_sheet_config and field_name in from_sheet_config:
                        col_index = from_sheet_config[field_name]

                    if col_index is None:
                        return self.fail("配置有误，来源配置 {from_service_name} sheet中不存在 {name} 列 ".format(
                            from_service_name=from_service_name, name=str(field_name)))
                    if col_index > len(rowValues):
                        return self.fail("配置有误，文件sheet中不存在 {col_index} 列 ".format(col_index=str(col_index)))
                    field_name = field["value"]

                    field_value = rowValues[col_index]
                    data_obj[field_name] = field_value
                data_list.append(data_obj)

        return self.success(data_list)
