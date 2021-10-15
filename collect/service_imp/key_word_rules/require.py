# -*- coding: utf-8 -*-
"""
@Time: 2021/6/28 15:49
@Author: zzhang zzhang@cenboomh.com
@File: require.py
@desc:
"""
from collect.collect_service import CollectService


class Require(CollectService):
    def __init__(self, op_user=None):
        """
        引入文件
        """
        CollectService.__init__(self, op_user)

    def get_replace_sql(self, sql_content, reg, c_dir):
        import re
        require_sql_list = re.findall(reg, sql_content)

        def get_sql_path(require_sql):
            require_sql_file_name = require_sql.replace("\"", "").replace("'", "").strip()
            require_sql_path = c_dir + "/" + require_sql_file_name
            return require_sql_path

        for require_sql in require_sql_list:
            require_sql_path = get_sql_path(require_sql)
            import os
            if not os.path.exists(require_sql_path):
                self.log(require_sql + "不存在", "error")
                return self.fail("依赖文件 " + require_sql + "文件不存在")

            with open(require_sql_path, 'r') as f:
                require_sql_file_content = f.read()
            require_sql_sub_list = re.findall(reg, require_sql_file_content)
            if len(require_sql_sub_list) > 0:
                sub_result = self.get_replace_sql(require_sql_file_content, reg, c_dir)
                if not self.is_success(sub_result):
                    return sub_result
                require_sql_file_content = self.get_data(sub_result)
            sql_content = sql_content.replace("require({require_sql})".format(require_sql=require_sql),
                                              require_sql_file_content)
        return self.success(sql_content)

    def handler(self, template, sql_file_content, params, config_rule, config_dir):
        sql_content_result = self.get_replace_sql(sql_file_content, config_rule["reg"], config_dir)
        if not self.is_success(sql_content_result):
            return sql_content_result
        sql_file_content = self.get_data(sql_content_result)
        return self.success(sql_file_content)
