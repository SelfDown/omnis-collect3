# -*- coding: utf-8 -*-
"""
@Time: 2021/6/28 16:59
@Author: zzhang zzhang@cenboomh.com
@File: template_data.py
@desc:
"""
from rest_framework.views import APIView

from collect.utils.collect_utils import Result, get_safe_data


class TemplateData(APIView):

    def post(self, request):
        data = request.data
        service = get_safe_data("service", data)
        if not service:
            return Result.fail_response(msg="服务不能为空")

        user_id = get_safe_data("user_id", request.session, "-1")
        from collect.service.template_service import TemplateService
        template = TemplateService(op_user=user_id)
        # 设置session
        template.set_session(request.session)
        # 获取结果
        data_result = template.result(data, is_http=True)
        if not template.is_success(data_result):
            return Result.fail_response(msg=template.get_msg(data_result))
        data = template.get_data(data_result)
        from django.http import FileResponse
        # 如果是个文件类型
        if isinstance(data, FileResponse):
            return data
        count = template.get_count(data_result)
        msg = template.get_msg(data_result)
        other = template.get_other(data_result)
        return Result.success_response(data=data, count=count, msg=msg, other=other)
