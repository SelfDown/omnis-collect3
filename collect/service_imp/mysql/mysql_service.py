# -*- coding: utf-8 -*-
"""
@Time: 2020/12/8 11:15
@Author: zzhang zzhang@cenboomh.com
@File: mysql_service.py
@desc:
"""
from collect.collect_service import CollectService
from collect.utils.collect_utils import is_empty, get_safe_data, sqlToData, connection_sql_to_data


class MysqlService(CollectService):
    def __init__(self, op_user):
        CollectService.__init__(self, op_user)

        pass

    def sql_file2sqlContent(self, sql_file, params):
        config_file_result = self.get_config_file(sql_file, params)
        if not self.is_success(config_file_result):
            self.log(self.get_msg(config_file_result), level="error")
            return
        return self.get_data(config_file_result)
        # import os
        # config_dir = self.get_config_dir()
        # sql_file = config_dir + "/" + sql_file
        # if not os.path.exists(sql_file):
        #     self.log(sql_file + "不存在", "error")
        #     return self.fail(sql_file + "文件不存在")
        # with open(sql_file, 'r') as f:
        #     sql_file_content = f.read()
        # key_word_rules = self.get_key_word_rules()
        # for key_word in key_word_rules:
        #     config_rule = key_word_rules[key_word]
        #     path = config_rule["path"]
        #     class_name = config_rule["class_name"]
        #     import importlib
        #     key_rule_class = importlib.import_module(path)
        #     key_rule_class = getattr(key_rule_class, class_name)()
        #     rule_result = key_rule_class.handler(self.template, sql_file_content, params, config_rule, config_dir)
        #     if not self.is_success(rule_result):
        #         return rule_result
        #     sql_file_content = self.get_data(rule_result)
        # return sql_file_content

    def content2Sql(self, sql_content, params, to_param_key=True, from_config=False):
        """

        :param sql_content: sql 内容
        :param params: 参数
        :param to_param_key: 保持变量
        :param from_config: 变量来着配置
        :return:
        """
        if not params:
            params = {}
        from django.template import Context, Template
        t = Template(sql_content)
        param_keys = []
        node_list = t.compile_nodelist()

        def append_var_name(node):
            if node.token.token_type == 1:
                param_keys.append(node.token.contents)

        def get_node_name_list(node_list):
            for node in node_list:
                append_var_name(node)
                if hasattr(node, 'nodelist'):
                    get_node_name_list(node.nodelist)

        # 递归获取
        get_node_name_list(node_list)
        #     for node_child in node.nodelist:
        #         # 解析第二层
        #         append_var_name(node_child)
        #         if hasattr(node_child, 'nodelist'):
        #             # 解析第三层
        #             for node_child_child in node_child.nodelist:
        #                 append_var_name(node_child_child)
        template_params = {}
        # 变量赋值 %s

        for param_key in param_keys:
            if from_config or not is_empty(param_key, params):  # 如果来着请求
                if to_param_key:
                    param_key_value = "{{" + param_key + "}}"
                else:
                    pkv = params[param_key]
                    # key 支持数组
                    if isinstance(pkv, list):
                        param_key_value = ",".join(["%s"] * len(pkv))
                    else:
                        param_key_value = '%s'
                template_params[param_key] = param_key_value

        # 其他字段直接copy
        for key in params:
            if key not in template_params:
                template_params[key] = params[key]

        c = Context(template_params)
        result_content = t.render(c)
        return result_content, param_keys

    def template2Sql(self, sql_content, params, from_config=False):

        try:
            # 转换为变量
            result_content, param_keys = self.content2Sql(sql_content, params, True, from_config)
            # 转换为sql的占位符
            result_content, param_keys = self.content2Sql(result_content, params, False, from_config)
            # 去掉html
            result_content = self.xml_to_plain_text(result_content)
            data = {
                self.get_sql_content_name(): result_content,
                self.get_sql_param_name(): param_keys
            }
            return self.success(data)
        except Exception as e:
            return self.fail(str(e) + "sql 解析错误")

    def get_sql(self, from_config=False):
        """
        这里只解析2级模板变量，意思是不支持if标签 里面在套用 if 标签
        :param params:  前台参数
        :param param_from:  生成sql 参数来着配置文件，还是请求参数
        :return:
        """
        sql_content = self.get_sql_content()
        count_sql_content = self.get_count_sql_content()

        # 如果存在sql,解析sql。如果是第一次加载，则从文件中获取。第二次缓存
        if not sql_content:
            sql_file = get_safe_data(self.get_sql_file_name(), self.template)
            sql_file_content = self.sql_file2sqlContent(sql_file, self.get_params_result())
            self.set_sql_content(sql_file_content)
            sql_content = sql_file_content

        sql_result = self.template2Sql(sql_content, self.get_params_result(), from_config)
        if not self.is_success(sql_result):
            return sql_result
        sql_result = self.get_data(sql_result)
        if not self.is_empty_count_sql():
            count_sql_file = get_safe_data(self.get_count_sql_name(), self.template)
            sql_count_file_content = self.sql_file2sqlContent(count_sql_file, self.get_count_params_result())
            self.set_count_sql_content(sql_count_file_content)
            count_sql_content = sql_count_file_content
        # 设置统计sql
        if count_sql_content:
            count_sql_result = self.template2Sql(count_sql_content, self.get_count_params_result(), from_config)
            if not self.is_success(count_sql_result):
                return count_sql_result
            count_sql_result = self.get_data(count_sql_result)
            sql_result[self.get_count_sql_name()] = count_sql_result[self.get_sql_content_name()]
            sql_result[self.get_count_sql_param_name()] = count_sql_result[self.get_sql_param_name()]
        return self.success(sql_result)

    def result_sql(self, result):
        """
        获取sql
        :param result:
        :return:
        """
        return result[self.get_sql_content_name()]

    def result_count_sql(self, result):
        """
        获取sql
        :param result:
        :return:
        """
        return result[self.get_count_sql_name()]

    def result_param(self, result):
        """
        获取参数
        :param result:
        :return:
        """
        return result[self.get_sql_param_data_name()]

    def result_param_name_list(self, result):
        """
        获取参数key 列表
        :param result:
        :return:
        """
        return result[self.get_sql_param_name()]

    def result_count_param_name_list(self, result):
        """
        获取count参数key 列表
        :param result:
        :return:
        """
        return result[self.get_count_sql_param_name()]

    def result(self, params=None):
        result = CollectService.result(self, params)
        if self.finish or not self.is_success(result):
            return result
        # from omnis_common.omnis_utils.utils import connection_sql_to_data
        sql_result = self.get_sql()
        if not self.is_success(sql_result):
            return sql_result
        sql_result = self.get_data(sql_result)
        sql = self.result_sql(sql_result)
        # 获取参数
        param_name_list = self.result_param_name_list(sql_result)
        param_data = []
        params = self.get_params_result()
        for p in param_name_list:
            if p in params:
                pkv = params[p]
                # 值支持数组
                if isinstance(pkv, list):
                    for item in pkv:
                        param_data.append(item)
                else:
                    param_data.append(params[p])
        if self.can_log():
            self.log(sql)
            self.log(param_data)
        data_source = self.get_data_source()
        result = connection_sql_to_data(sql, param_data, datasource=data_source)
        count = 0
        if not self.is_empty_count_sql():
            count_sql = self.result_count_sql(sql_result)
            count_params = self.get_count_params_result()
            count_param_name_list = self.result_count_param_name_list(sql_result)
            count_param_data = []

            for p in count_param_name_list:
                if p in count_params:
                    count_param_data.append(params[p])
            if self.can_log():
                self.log(count_sql)
                self.log(count_param_data)
            count_data = connection_sql_to_data(count_sql, count_param_data, datasource=data_source)
            if len(count_data) > 0:
                count_data = count_data[0]
                count = get_safe_data(self.get_count_name(), count_data)

        return self.success(result, count=count)
