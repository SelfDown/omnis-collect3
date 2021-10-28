# -*- coding: utf-8 -*-
"""
@Time: 2021/7/14 16:32
@Author: zzhang zzhang@cenboomh.com
@File: ModelUpdate.py
@desc:
"""
from collect.service_imp.model.model_delete import ModelDeleteService
from collect.utils.collect_utils import get_safe_data


class ModelUpdateService(ModelDeleteService):
    MUConst = {
        "update_fields_name": "update_fields"
    }

    def __init__(self, op_user):
        ModelDeleteService.__init__(self, op_user)

        pass

    def get_update_fields_name(self):
        return self.MUConst["update_fields_name"]

    def result(self, params=None):
        result = self.handler_model_params(params)
        if self.finish or not self.is_success(result):
            return result
        # 获取模型对象
        model_obj_result = self.get_model_obj()
        if not self.is_success(model_obj_result):
            return model_obj_result
        model_obj = self.get_data(model_obj_result)
        filter_result = self.get_model_filter()
        if not self.is_success(filter_result):
            return filter_result
        c = self.get_count(filter_result)
        query_filter = self.get_data(filter_result)
        u_fields = get_safe_data(self.get_update_fields_name(), self.get_template())
        es_fields = get_safe_data(self.get_exclude_save_field_name(), self.get_template())
        update_fields = self.get_update_fields(model_obj, update_fields=u_fields,
                                               exclude_save_field=es_fields)
        if len(update_fields) == 0:
            return self.fail(msg="没有找到更新字段")

        if c == 0:
            return self.fail(msg="没有找到更新记录")
        update_obj = {}
        params_result = self.get_params_result()
        for key in update_fields:
            update_obj[key] = params_result[key]

        update_sum = query_filter.update(**update_obj)
        if update_sum != c:
            return self.success(data=[], msg="总共修改【{c}】 条。修改 【{update_sum}】条记录成功".format(c=str(c),
                                                                                         update_sum=str(update_sum)))
        return self.success(data=[], msg="修改 【{c}】条记录成功".format(c=str(update_sum)), count=c)
