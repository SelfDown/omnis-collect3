# -*- coding: utf-8 -*-
"""
@Time: 2021/6/21 11:35
@Author: zzhang zzhang@cenboomh.com
@File: import_excel.py
@desc:
"""
from rest_framework.views import APIView

from collect.utils.collect_utils import get_safe_data


class ExcelImport(APIView):
    def post(self, request):

        data = request.data
        user_id = get_safe_data("user_id",request.session,"-1")
        from collect.service.excel_service import ExcelService
        excel_data = ExcelService(op_user=user_id)
        return excel_data.import_data(data)
