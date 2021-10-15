# -*- coding: utf-8 -*-
"""
@Time: 2021/8/4 14:17
@Author: zzhang zzhang@cenboomh.com
@File: new_col.py
@desc:
"""
from collect.service_imp.common.filters.template_tool import TemplateTool
from collect.service_imp.result_handlers.result_handler import ResultHandler
from collect.utils.collect_utils import get_safe_data


class NewCol(ResultHandler):
    nc_const = {
        "parent_name": "parent"
    }

    def get_parent_name(self):
        return self.nc_const["parent_name"]

    def handler(self, result, config, template):
        params = get_safe_data(self.get_params_name(), config)
        if not params:
            return self.fail("新列处理器没有找到 {params} 节点".format(params=self.get_params_name()))

        to_field = get_safe_data(self.get_to_field_name(), params)
        if not to_field:
            return self.fail("参数中没有找到" + self.get_to_field_name() + " 节点")
        field_parent = get_safe_data(self.get_field_name(), params)

        t = TemplateTool()
        for field_item in to_field:
            field = get_safe_data(self.get_field_name(), field_item)
            if not field:
                return self.fail("参数" + self.get_field_name() + " 节点,没有找到" + self.get_field_name())
            templ = get_safe_data(self.get_template_name(), field_item)
            if not templ:
                return self.fail("参数" + self.get_to_field_name() + " 节点,没有找到" + self.get_template_name())

            def set_value(obj):
                if templ in obj:
                    value = obj[templ]
                else:
                    value = t.render(templ, obj)
                obj[field] = value

            if isinstance(result, list):
                for item in result:
                    if not field_parent:
                        set_value(item)
                    elif field_parent in item:
                        children = item[field_parent]
                        # 对子进行赋值
                        for child in children:
                            p = self.get_parent_name()
                            before = None

                            if p in child:
                                before = child[p]
                            child[p] = item
                            set_value(child)
                            del child[p]
                            if before:
                                child[p] = before

            elif isinstance(result, dict):
                set_value(result)

        remove = get_safe_data(self.get_remove_name(), params)
        if remove:
            def remove_field(obj):
                for field in remove:
                    if field in obj:
                        del obj[field]

            if isinstance(result, list):
                for item in result:
                    if not field_parent:
                        remove_field(item)
                    elif field_parent in item:
                        children = item[field_parent]
                        for child in children:
                            remove_field(child)

            elif isinstance(result, dict):
                remove_field(result)
        return self.success(result)
