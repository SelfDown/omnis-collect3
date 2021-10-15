# -*- coding: utf-8 -*-
"""
@Time: 2021/8/31 9:03
@Author: zzhang zzhang@cenboomh.com
@File: mul_arr.py
@desc:
"""
from collect.service_imp.request_handlers.request_handler import RequestHandler
from collect.utils.collect_utils import get_safe_data


class MulArr(RequestHandler):
    ma_const = {
        "from_arr_name": "from_arr",
        "mul_arr_name": "mul_arr",
        "obj_name": "obj"
    }

    def get_from_arr_name(self):
        return self.ma_const["from_arr_name"]

    def get_mul_arr_name(self):
        return self.ma_const["mul_arr_name"]
    def get_obj_name(self):
        return self.ma_const["obj_name"]

    def handler(self, params, config, template):

        from_arr_name = get_safe_data(self.get_from_arr_name(), config)

        if not from_arr_name:
            return self.fail("数组乘法处理器没有找到 {field} 节点".format(field=self.get_from_arr_name()))
        mul_arr_name = get_safe_data(self.get_mul_arr_name(), config)
        if not mul_arr_name:
            return self.fail("数组乘法处理器没有找到 {field} 节点".format(field=self.get_mul_arr_name()))

        obj = get_safe_data(self.get_obj_name(), config)
        if not obj:
            return self.fail("数组乘法处理器没有找到 {field} 节点".format(field=self.get_obj_name()))
        save_field = get_safe_data(self.get_save_field_name(), config)
        if not save_field:
            return self.fail("数组乘法处理器没有找到 {field} 节点".format(field=self.get_save_field_name()))
        from_arr = get_safe_data(from_arr_name,params)
        if not from_arr:
            return self.fail("参数没有找到 {field} 节点".format(field=from_arr))
        mul_arr = get_safe_data(mul_arr_name,params)
        if not mul_arr:
            return self.fail("参数没有找到 {field} 节点".format(field=mul_arr))
        result_list = []
        from collect.service_imp.common.filters.template_tool import TemplateTool
        tool = TemplateTool(op_user=self.op_user)
        import copy
        # 数组乘以数组
        for from_item in from_arr:
            t = {"from_item":from_item}
            for mul_item in mul_arr:
                result = copy.deepcopy(mul_item)
                for key in obj:
                    temp = obj[key]
                    v = self.get_render_data(temp,t,tool)
                    result[key]=v
                result_list.append(result)

        params[save_field] = result_list
        return self.success(params)
