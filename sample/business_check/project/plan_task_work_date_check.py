# -*- coding: utf-8 -*-
"""
@Time: 2021/7/19 15:22
@Author: zzhang zzhang@cenboomh.com
@File: plan_task_work_date_check.py
@desc:
"""
from collect.service_imp.request_rules.check import CheckData


class WorkDateCheck(CheckData):
    def handler(self, params, config_params, template=None):

        from collect.service.template_service import TemplateService
        template = TemplateService(op_user=self.op_user)
        params["service"] = "project_manage.plan_task_project_per_query"
        data_result = template.result(params)
        if not self.is_success(data_result):
            return False, self.get_msg(data_result)
        arr = self.get_data(data_result)
        if arr and len(arr) > 0:
            msg_list = []
            for item in arr:
                msg = "{project_ids} {date}已经达到 {current_sum} % 了".format(project_ids=item["project_ids"],
                                                                          date=str(item["date"]),
                                                                          current_sum=str(item["current_sum"]))
                msg_list.append(msg)
            return False, [], "\n".join(msg_list)

        return True, [], "检查通过"
