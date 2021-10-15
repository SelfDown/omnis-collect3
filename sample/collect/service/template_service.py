# -*- coding: utf-8 -*-
"""
@Time: 2021/6/28 17:01
@Author: zzhang zzhang@cenboomh.com
@File: template_service.py
@desc:
"""
from collect.collect_service import CollectService
from collect.utils.collect_utils import get_safe_data


class TemplateService(CollectService):
    def __init__(self, op_user=None):
        CollectService.__init__(self, op_user)
        self.op_user = op_user
        self.session = None

    def set_session(self, session):
        self.session = session

    def get_session(self):
        return self.session

    def result(self, data):

        service = get_safe_data("service", data)
        if not service:
            return self.fail("服务不能为空")
        collect_service = CollectService(op_user=self.op_user)
        collect_service.set_session(self.get_session())
        result = collect_service.make_service(service)

        if not collect_service.is_success(result):
            return result

        service_obj = collect_service.get_data(result)
        # 查询数据
        params = data
        # 所有接口必须登录检查
        login_check = service_obj.login_check()
        if not collect_service.is_success(login_check):
            return login_check
        # 执行前处理
        before_result = service_obj.before_result(params)
        if not service_obj.is_success(before_result) or self.is_finish(before_result):
            return before_result
        # 执行结果
        return_result = service_obj.result(params)
        if not service_obj.is_success(return_result):
            return return_result
        data = service_obj.get_data(return_result)
        count = service_obj.get_count(return_result)
        msg = service_obj.get_msg(return_result)
        # 获取结果后处理器
        after_result = service_obj.after_result(data)
        if not self.is_success(after_result):
            return after_result
        # 设置处理之后的结果
        data = self.get_data(after_result)
        # 获取处理之后的消息
        after_msg = self.get_msg(after_result)
        if after_msg:
            msg = after_msg
        return self.success(data, msg=msg, count=count)
