# -*- coding: utf-8 -*-
# templ = "{% if is_windows== 'True' %}get_host{% else %}agentd_soft_install{% endif %}"
# # templ = "get_host"
# print templ
# print "-----------------------------------------------------------"
#
#
# def get_template_nodes(templ):
#     from jinja2 import Environment
#     env = Environment()
#     parsed_content = env.parse(templ)
#     content = parsed_content.body
#     result = []
#
#     def get_node(node):
#         node_list = []
#         if hasattr(node, "nodes"):
#             nodes = getattr(node, "nodes")
#             for node in nodes:
#                 data = getattr(node, "data")
#                 node_list.append(data)
#         for l in "body", "elif_", "else_":
#             node_list += get_nodes(node, l)
#         return node_list
#
#     def get_nodes(parent_node, name):
#         node_list = []
#         if not hasattr(parent_node, name):
#             return node_list
#         body = getattr(parent_node, name)
#         for child in body:
#             node_list += get_node(child)
#         return node_list
#
#     for item in content:
#         result += get_node(item)
#     return result
#
#
# print get_template_nodes(templ)
import collect.service_imp.request_rules.check
import collect.service_imp.before_plugin.plugin.handler_params
import collect.service_imp.request_handlers.handlers.service2field
import collect.service_imp.key_word_rules.require
# collect.service_imp.before_plugin.plugin.handler_params

import collect.service_imp.flow.common.gen_template
import collect.service_imp.request_rules.template
import collect.service_imp.common.filters.template_filters.json_str
import collect.service_imp.flow.common.scp_copy
import collect.service_imp.flow.omnis_ssh

