# -*- coding: utf-8 -*-
"""
@Time: 2021/8/4 13:43
@Author: zzhang zzhang@cenboomh.com
@File: array_2_obj.py
@desc:
"""
from collect.service_imp.common.filters.template_tool import TemplateTool
from collect.service_imp.result_handlers.result_handler import ResultHandler
from collect.utils.collect_utils import get_safe_data


class Array2Obj(ResultHandler):
    def handler(self, result, config, template):
        params = get_safe_data(self.get_params_name(), config)
        # 如果是空对象，直接返回
        if not result or len(result) <= 0:

            result = {}
            if params:
                field = get_safe_data(self.get_field_name(), params)
                if field:
                    result[field] = {}
            return self.success(result)

        # field = get_safe_data(self.get_field_name(), params)

        result_obj = None
        if not params:
            if not isinstance(result, list):
                return self.fail("结果对象不是数组，请检查返回结果")
            result_obj = result[0]
        else:
            field = get_safe_data(self.get_field_name(), params)
            # result_obj = result
            tool = TemplateTool(op_user=self.op_user)
            param_result = self.get_params_result(template)

            def parse_obj(obj, field=None):
                # 如果有字段，就取字段对象
                import copy
                if field:
                    if len(obj[field]) > 0:
                        target = copy.copy(obj[field][0])
                    else:
                        target = {

                        }

                else:
                    target = copy.copy(obj)
                # 赋值 请求参数
                if isinstance(target, dict):
                    target[str(self.get_params_result_name())] = param_result
                if field:
                    obj[field] = target
                else:
                    obj = target
                if isinstance(target, dict):
                    del target[str(self.get_params_result_name())]
                # 进行模板赋值
                to_field = get_safe_data(self.get_to_field_name(), params)
                if to_field:
                    for field_item in to_field:
                        field_name = get_safe_data(self.get_field_name(), field_item)
                        # templ = get_safe_data(self.get_template_name(), field_item)
                        node_result = self.get_node_template_result(field_item, obj, template=template)
                        if not self.is_success(node_result):
                            return node_result
                        v = self.get_data(node_result)
                        # v = tool.render(templ, target)
                        obj[field_name] = v
                return self.success(obj)

            # 针对字段进行转对象
            if field:
                if isinstance(result, list):
                    for index, item in enumerate(result):
                        if field not in item:
                            return self.fail("结果数据列表，第【" + str(index + 1) + "】对象里面，没有找到" + field + " 字段")
                        if not isinstance(item[field], list):
                            return self.fail("结果数据列表，第【" + str(index + 1) + "】对象里面，" + field + " 字段不是数组")

                        obj_result = parse_obj(item, field)
                        if not self.is_success(obj_result):
                            return obj_result
                    result_obj = result
                if isinstance(result, dict):
                    if field not in result:
                        return self.fail("结果数据对象里面，没有找到" + field + " 字段")
                    obj_result = parse_obj(result, field)
                    if not self.is_success(obj_result):
                        return obj_result
                    result_obj = self.get_data(obj_result)

            else:
                if not isinstance(result, list):
                    return self.fail("结果对象不是数组，请检查返回结果")
                # result_obj = parse_obj(result[0])
                obj_result = parse_obj(result[0])
                if not self.is_success(obj_result):
                    return obj_result
                result_obj = self.get_data(obj_result)

        return self.success(result_obj)

        # # 如果没有参数，返回第一个数据
        # if not params:
        #     if isinstance(result, list):
        #         return self.success(result[0])
        #     else:
        #         return self.success(result)
        #
        # # 如果存在字段，转field 的字段
        # if not field:
        #     if isinstance(result, list):
        #         return self.success(result[0])
        # else:
        #
        #     if isinstance(result, list):
        #         result_list = []
        #         for item in result:
        #             result_list.append(parse_obj(item))
        #         return self.success(result_list)
        #     elif isinstance(result, dict):
        #         result = parse_obj(result)
        #         return self.success(result)
        #     else:
        #         return self.success(result)
