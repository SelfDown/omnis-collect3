# -*- coding: utf-8 -*-
"""
@Time: 2021/7/26 14:00
@Author: zzhang zzhang@cenboomh.com
@File: bulk_create.py
@desc:
"""
from collect.collect_service import CollectService
from collect.utils.collect_utils import get_safe_data


class BulkCreateService(CollectService):
    def __init__(self, op_user):
        CollectService.__init__(self, op_user)

        pass

    def result(self, params=None):
        result = CollectService.result(self, params)
        if self.finish or not self.is_success(result):
            return result
        params_result = self.get_params_result()
        models = get_safe_data(self.get_model_field_name(), self.template)
        models_result = get_safe_data(models, params_result)
        if not models_result:
            return self.fail("没有新增数据对象")
        model_obj_result = self.get_model_obj()
        if not self.is_success(model_obj_result):
            return model_obj_result
        model_list = []
        for param in models_result:
            model_obj_result = self.get_model_obj()
            model_obj = self.get_data(model_obj_result)
            # 更新字段
            model_obj_result = self.update_field(model_obj, param)
            if not model_obj_result:
                return model_obj_result
            model_list.append(self.get_data(model_obj_result))
        model_class = self.get_model_class()
        try:
            model_class.objects.bulk_create(model_list)
        except Exception as e:
            return self.fail(str(e) + "创建失败")

        return self.success(params)
