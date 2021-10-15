# -*- coding: utf-8 -*-
"""
@Time: 2021/7/28 10:54
@Author: zzhang zzhang@cenboomh.com
@File: log.py
@desc:
"""
import logging

_collect_tmp_logger = None


def get_collect_log(file_name="./logs/collect.log"):
    global _collect_tmp_logger
    if _collect_tmp_logger:
        return _collect_tmp_logger

    import os
    log_dir = os.path.dirname(file_name)
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)

    # 创建日志的实例
    logger = logging.getLogger("logger")
    # 指定Logger的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    # 创建日志：
    # 文件日志

    # 终端日志

    # 设置默认的日志级别
    logger.setLevel(logging.DEBUG)
    # 把文件日志和终端日志添加到日志处理器中
    if len(logger.handlers) <= 0:
        file_handler = logging.FileHandler(file_name)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    if len(logger.handlers) <= 1:
        import sys
        consle_handler = logging.StreamHandler(sys.stdout)
        consle_handler.setFormatter(formatter)
        logger.addHandler(consle_handler)

    _collect_tmp_logger = logger
    return logger
