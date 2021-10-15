# -*- coding: utf-8 -*-
"""
@Time: 2021/7/14 16:32
@Author: zzhang zzhang@cenboomh.com
@File: ModelUpdate.py
@desc:
"""
from collect.service_imp.model.model_save import ModelSaveService
from collect.utils.collect_utils import get_safe_data


class ModelDeleteService(ModelSaveService):
    def __init__(self, op_user):
        ModelSaveService.__init__(self, op_user)

        pass

    def result(self, params=None):
        result = self.handler_model_params(params)
        if self.finish or not self.is_success(result):
            return result
        # 获取模型对象
        model_obj_result = self.get_model_obj()
        if not self.is_success(model_obj_result):
            return model_obj_result
        model_class = self.get_model_class()
        filter = get_safe_data(self.get_filter_name(), self.template)
        if not filter:
            return self.fail(msg="没有配置过滤条件，不能删除")
        f = {}
        for key in filter:
            param_key = filter[key]
            if param_key not in params:
                return self.fail(param_key + "字段不存在！")
            f[key] = params[param_key]
        query_filter = model_class.objects.filter(**f)
        c = query_filter.count()
        if c > 1000:
            return self.fail(msg="结果超过1000，不能删除")
        delete_sum, data = query_filter.delete()
        if delete_sum != c:
            return self.success(data=[], msg="总共删除【{c}】 条。删除 【{delete_sum}】条记录成功".format(c=str(c),
                                                                                         delete_sum=str(delete_sum)))
        return self.success(data=[], msg="删除 【{c}】条记录成功".format(c=str(delete_sum)))
