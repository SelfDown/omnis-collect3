# -*- coding: utf-8 -*-
"""
@Time: 2021/7/14 16:32
@Author: zzhang zzhang@cenboomh.com
@File: ModelUpdate.py
@desc:
"""
from collect.collect_service import CollectService
from collect.utils.collect_utils import get_safe_data


class ModelSaveService(CollectService):
    def __init__(self, op_user):
        CollectService.__init__(self, op_user)

        pass

    def get_exclude_save_field_name(self):
        return self.const["exclude_save_field_name"]

    def get_exclude_save_field(self):
        return get_safe_data(self.get_exclude_save_field_name(), self.template)

    def handler_model_params(self, params):
        return CollectService.result(self, params)

    def validate_model(self, model_obj):
        from django.core.exceptions import ValidationError
        try:
            model_obj.full_clean()
        except ValidationError as e:
            msg_list = []
            md = e.message_dict
            for field_key in md:
                template_params = self.get_template_params()
                param = get_safe_data(field_key, template_params)
                name = field_key
                detail = md[field_key]
                if param:
                    n = get_safe_data("name", param)
                    if n:
                        name = n
                msg = "字段 【{name}】错误： {detail}".format(name=name, detail=" ".join(detail))
                msg_list.append(msg)
            return self.fail(msg=",".join(msg_list))
        return self.success(model_obj)

    def result(self, params=None):
        result = self.handler_model_params(params)
        if self.finish or not self.is_success(result):
            return result
        import time
        start = time.time()
        # 获取模型对象
        model_obj_result = self.get_model_obj()
        if not self.is_success(model_obj_result):
            return model_obj_result
        model_obj = self.get_data(model_obj_result)
        # 更新字段
        model_obj_result = self.update_field(model_obj)
        if not self.is_success(model_obj_result):
            return model_obj_result
        # 校验数据
        model_obj_result = self.validate_model(model_obj)
        if not model_obj_result:
            return model_obj_result
        # 保存
        fields = {}
        exclude_save_field = self.get_exclude_save_field()
        if exclude_save_field:  # 去掉不可以修改的字段

            update_fields = self.get_update_fields(model_obj)
            update_fields = [i for i in update_fields if i not in exclude_save_field]
            if len(update_fields) > 0:
                fields["update_fields"] = update_fields

            model_obj.save(**fields)
        else:
            model_obj.save()
        param_result = self.get_params_result()
        end = time.time()
        if self.can_log():
            service_name = get_safe_data(self.get_service_name(), params)
            self.log("{service} 保存耗时 {spend}".format(service=service_name, spend=str(end - start)))

        def getDict():
            fields = []
            for field in model_obj._meta.fields:
                fields.append(field.name)

            d = {}

            def isAttrInstance(attr, clazz):
                return isinstance(getattr(model_obj, attr), clazz)
            import datetime
            for attr in fields:
                if isinstance(getattr(model_obj, attr), datetime.datetime):
                    d[attr] = getattr(model_obj, attr).strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(getattr(model_obj, attr), datetime.date):
                    d[attr] = getattr(model_obj, attr).strftime('%Y-%m-%d')
                elif isAttrInstance(attr, int) or isAttrInstance(attr, float) \
                        or isAttrInstance(attr, str):
                    d[attr] = getattr(model_obj, attr)
                # else:
                #   d[attr] = getattr(self, attr)

            return d

        return self.success(data=getDict(), msg="保存成功")
