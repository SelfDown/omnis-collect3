# -*- coding: utf-8 -*-
"""
@Time: 2021/8/19 17:57
@Author: zzhang zzhang@cenboomh.com
@File: bulk_service.py
@desc:
"""
from collect.collect_service import CollectService
from collect.utils.collect_utils import get_safe_data
import threading


class BulkThread(threading.Thread):
    def __init__(self, func, args=()):
        super(BulkThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None


class BulkThreadList():
    """
     获取线程运行同一个方法
    """

    def __init__(self, func, max_once=30):
        """

        :param func:  运行方法
        :param max_once:  单次运行个数
        """
        self.func = func
        self.args_list = []
        self.li = []
        self.max_once = max_once

    def add_data(self, args=()):

        th = BulkThread(func=self.func, args=args)
        self.li.append(th)

    def get_results(self):
        """
        防止钉钉请求数过大，将请求成{max_once}个一组
        :return:
        """
        results = []
        start = 0
        for th_item in range(0, len(self.li), self.max_once):
            uli = self.li[start:th_item + self.max_once]
            start = th_item + self.max_once
            for item in uli:
                item.start()
            for item in uli:
                item.join()
                result = item.get_result()
                results.append(result)

        self.li = []
        return results


class ServiceBulkService(CollectService):
    bs_const = {
        "batch_name": "batch",
        "item_name": "item"
    }

    def get_item_name(self):
        return self.bs_const["item_name"]

    def get_batch_name(self):
        return self.bs_const["batch_name"]

    def get_batch(self):
        return get_safe_data(self.get_batch_name(), self.template)

    def __init__(self, op_user):
        CollectService.__init__(self, op_user=op_user)

    def get_node_result(self, node, params, template):

        service_data = self.get_node_service(node=node, params=params, template=template,
                                             append_param=True)
        if not service_data:
            return service_data
        service = self.get_data(service_data)
        service_result = self.get_service_result(service, self.template)
        return service_result

    def result(self, params):
        params_result = self.get_params_result()
        batch = self.get_batch()
        if not batch:
            return self.fail("配置中没有找到【" + self.get_batch_name() + "】标签")

        foreach_name = get_safe_data(self.get_foreach_name(), batch)
        if not foreach_name:
            return self.fail("配置中没有找到【" + self.get_foreach_name() + "】标签")
        foreach = get_safe_data(foreach_name, params_result)
        if not foreach:
            return self.fail("参数中没有找到【" + foreach_name + "】变量")
        item_name = get_safe_data(self.get_item_name(), batch)
        if not item_name:
            return self.fail("配置中没有找到【" + self.get_item_name() + "】标签")

        result_list = []
        btl = BulkThreadList(func=self.get_node_result)
        if len(foreach)>100:
            return self.fail("服务不能超过100个")
        if self.can_log():
            self.log("总共运行" + str(len(foreach)) + "服务")


        for index, item in enumerate(foreach):
            import copy
            batch_tmp = copy.deepcopy(batch)
            params_tmp = copy.deepcopy(params_result)
            if self.can_log():
                self.log(self.get_template_service_name() + "添加第 " + str(index + 1) + " 个服务")
            params_tmp[item_name] = item
            btl.add_data(args=(batch_tmp, params_tmp, self.template))
        results = btl.get_results()
        for service_result in results:
            result_list.append(service_result)
        save_field = get_safe_data(self.get_save_field_name(), batch)
        if save_field:
            params_result[save_field] = result_list
        return self.success({})
