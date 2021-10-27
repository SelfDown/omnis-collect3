# -*- coding: utf-8 -*-
"""
@Time: 2021/6/28 16:09
@Author: zzhang zzhang@cenboomh.com
@File: config_cache_data.py
@desc:
"""

# 路由
from collect.utils.collect_utils import get_safe_data

router_config = None
# 数据转换规则
rules = None
# 模板关键字
key_word_rules = None
# sql 模板数据
sql_template_cache = {}

# 请求字段规则
request_rules = None

# django model 配置
django_model_config = None
# 请求处理器
request_handler = None
# 结果处理器
result_handler = None
# 模块处理器 = None
module_handler = None
# 模板自定义函数
filter_handler = None
# 请求插件
before_plugin = None
# 结果插件
after_plugin = None

# 第三方插件
third_application=None

class ConfigCacheData:
    """
     获取配置缓存数据，可以将这个数据做成缓存，这里使用全局变量
    """

    def __init__(self):
        """

        """

    @staticmethod
    def get_sql(key):
        global sql_template_cache
        return get_safe_data(key, sql_template_cache)

    @staticmethod
    def set_sql(key, content):
        global sql_template_cache
        sql_template_cache[key] = content

    @staticmethod
    def set_router_config(router_config_data):
        global router_config
        router_config = router_config_data

    @staticmethod
    def get_router_config():
        """
        获取路由规则
        :return:
        """
        global router_config
        import copy
        return copy.deepcopy(router_config)
        # return router_config

    @staticmethod
    def get_rules():
        """
        获取数据结果转换规则
        :return:
        """
        global rules
        return rules

    @staticmethod
    def set_rules(rules_data):
        global rules
        rules = rules_data

    @staticmethod
    def get_django_model_config():
        """
        获取django model 配置
        :return:
        """
        global django_model_config
        return django_model_config

    @staticmethod
    def set_django_model_config(django_model_config_data):
        global django_model_config
        django_model_config = django_model_config_data

    @staticmethod
    def get_key_word_rules():
        """
        获取关键字规则
        :return:
        """
        global key_word_rules
        return key_word_rules

    @staticmethod
    def set_key_word_rules(key_word_rule_data):
        """
        设置关键字
        :return:
        """
        global key_word_rules
        key_word_rules = key_word_rule_data

    @staticmethod
    def set_request_rules(request_rules_data):
        global request_rules
        request_rules = request_rules_data

    @staticmethod
    def get_request_rules():
        global request_rules
        return request_rules

    @staticmethod
    def set_request_handler(request_handler_data):
        global request_handler
        request_handler = request_handler_data

    @staticmethod
    def get_request_handler():
        global request_handler
        return request_handler

    @staticmethod
    def set_result_handler(result_handler_data):
        global result_handler
        result_handler = result_handler_data

    @staticmethod
    def get_result_handler():
        global result_handler
        return result_handler

    @staticmethod
    def set_module_handler(module_handler_data):
        global module_handler
        module_handler = module_handler_data

    @staticmethod
    def get_module_handler():
        global module_handler
        return module_handler
    @staticmethod
    def set_filter_handler(filter_handler_data):
        global filter_handler
        filter_handler = filter_handler_data

    @staticmethod
    def get_filter_handler():
        global filter_handler
        return filter_handler

    @staticmethod
    def set_before_plugin(before_plugin_data):
        global before_plugin
        before_plugin = before_plugin_data

    @staticmethod
    def get_before_plugin():
        global before_plugin
        return before_plugin


    @staticmethod
    def set_after_plugin(after_plugin_data):
        global after_plugin
        after_plugin = after_plugin_data

    @staticmethod
    def get_after_plugin():
        global after_plugin
        return after_plugin

    @staticmethod
    def set_third_application(third_application_data):
        global third_application
        third_application = third_application_data

    @staticmethod
    def get_third_application():
        global third_application
        return third_application
