# -*- coding: utf-8 -*-
"""
@Time: 2021/6/23 10:09
@Author: zzhang zzhang@cenboomh.com
@File: mysql_update.py
@desc:
"""
import threading

from collect.service_imp.mysql.mysql_service import MysqlService
from collect.utils.collect_utils import get_safe_data, executeSQLMany


class MysqlUpdateService(MysqlService):
    """
    mysql 更新
    """

    def __init__(self, op_user):
        MysqlService.__init__(self, op_user)

    def handler_sql_params(self, param):
        """
        将数据处理成sql ,和长沙
        :param param:
        :return:
        sql_content sql 内容
        sql_param_data 参数值列表
        """
        # 重新设置param_result
        params_result = self.handler_req_params({})
        if not self.is_success(params_result):
            return params_result
        params_result = self.get_data(params_result)
        self.set_params_result(params_result)
        sql_result = self.get_sql(from_config=True)
        if not self.is_success(sql_result):
            return sql_result
        sql_result = self.get_data(sql_result)
        sql_param = sql_result[self.get_sql_param_name()]
        excel_result = get_safe_data(self.get_excel_result_name(), param)
        if len(excel_result) <= 0:
            return self.fail(msg="请检查导入文件，没有数据")
        data_first = excel_result[0]
        for field in sql_param:
            if field not in data_first:
                return self.fail(msg="{field} 字段在数据中没有，请检查配置".format(field=field))
        param_list = []
        for item in excel_result:
            param_data = []
            for field in sql_param:
                param_data.append(item[field])
            param_list.append(param_data)
        sql_result[self.get_sql_param_data_name()] = param_list
        return self.success(sql_result)

    def result(self, params=None):
        sql_param_result = self.handler_sql_params(params)
        if not self.is_success(sql_param_result):
            return sql_param_result
        sql_param_result = self.get_data(sql_param_result)
        sql = self.result_sql(sql_param_result)
        param = self.result_param(sql_param_result)
        update_num = "更新数量{num}".format(num=str(len(param)))
        if self.can_log():
            self.log(sql)
            self.log(update_num)
        if self.is_async():
            t = threading.Thread(target=executeSQLMany, args=(sql, param))
            t.start()
            msg = "正在异步更新，请稍后;更新数量{count}".format(count=str(update_num))
            return self.success(msg)
        else:
            count = executeSQLMany(sql, param)
            msg = "更新成功;更新{count}".format(count=str(count))
            return self.success(msg)
