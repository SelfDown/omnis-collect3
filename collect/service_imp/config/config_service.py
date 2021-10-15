# -*- coding: utf-8 -*-
"""
@Time: 2021/7/14 16:32
@Author: zzhang zzhang@cenboomh.com
@File: ModelUpdate.py
@desc:
"""
from collect.collect_service import CollectService


class ConfigService(CollectService):

    def __init__(self, op_user):
        CollectService.__init__(self, op_user)
        pass



    def result(self, params=None):
        config_data = self.get_config_data()
        tree = []
        count = 0
        for key in config_data:
            group = {"key": key,
                     "iconSkin": "insight-file",
                     "children": []}
            services = config_data[key]
            for child_key in services:
                child = services[child_key]
                child["iconSkin"] = "insight-service"
                group["children"].append(child)
                count += 1
            tree.append(group)
        return self.success(data=tree, count=count)
