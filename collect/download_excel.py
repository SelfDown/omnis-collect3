# -*- coding: utf-8 -*-
'''
@author: zzhang zzhang@cenboomh.com
@file: views.py
@time: 2020/9/2 17:58
@desc:
'''
from rest_framework.views import APIView

from collect.utils.collect_utils import get_safe_data


class ExcelDownload(APIView):
    def get(self, request):
        data = request.query_params
        user_id = get_safe_data("user_id",request.session,"-1")
        from collect.service.excel_service import ExcelService
        excel_data = ExcelService(op_user=user_id)
        return excel_data.download(data)

        # return Result.file_response("./template/allowance.xls","test.xls")
