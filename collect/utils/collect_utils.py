# -*- coding: utf-8 -*-
"""
@Time: 2021/7/28 10:43
@Author: zzhang zzhang@cenboomh.com
@File: collect_utils.py
@desc:
"""
import datetime
import json
import os

from django.http import HttpResponse

from collect.utils.property import Properties

fact_item_config = './conf/application.properties'
#  这里判断文件是否存在
if not os.path.exists(fact_item_config):
    raise Exception("根目下没有找到" + fact_item_config + "文件", )
props = Properties(fact_item_config)  # 读取文件


def getDateTime():
    import time
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


class data_value_check:

    @staticmethod
    def not_obj(name, data):
        if name not in data:
            return True
        value = data[name]
        if not isinstance(value, object):
            return True
        return False

    # 判断是否为空，为空返回 False
    @staticmethod
    def not_list(name, data):
        if name not in data:
            return True
        value = data[name]
        if not isinstance(value, list):
            return True
        return False

    # 判断是否为空，为空返回 False
    @staticmethod
    def not_empty(name, data):
        if name not in data or not data[name]:
            return True
        return False

    # 判断是否整形，否 True
    @staticmethod
    def not_int(name, data):
        if name not in data:
            return True

        try:
            int(data[name])
        except ValueError:
            return True

        return False

    @staticmethod
    def not_int_can_null(name, data):
        if name not in data:
            return False
        if not data[name]:
            return False
        try:
            int(data[name])
        except ValueError:
            return True

        return False


class OmnisService:
    """
    服务查询状态结果返回，
    主要包括3个字段
    第一,服务调用成功的状态
    第二，主体数据域
    第三，count 总体数据量
    """
    success_code = "0"
    fail_code = "1"

    def __init__(self):
        pass

    @staticmethod
    def get_other(result):
        return get_safe_data("other", result)



    @staticmethod
    def success(data=[], msg="查询成功", count=-1, finish=False, other=None):
        result = {
            "code": OmnisService.success_code,
            "success": True,
            "data": data,
            "msg": msg
        }
        if count != -1:
            result["count"] = count

        # 是否结束标志
        if finish:
            result["finish"] = finish
        # 其他字段标志
        if other:
            result["other"] = other
        return result

    @staticmethod
    def fail(data=[], code="1", msg=""):
        result = {"code": code, "msg": msg, "success": False, 'data': data}
        return result

    @staticmethod
    def get_count(result):
        return get_safe_data("count", result, 0)

    @staticmethod
    def is_success(result):
        return result["success"]

    @staticmethod
    def is_finish(result):
        return get_safe_data("finish", result)

    @staticmethod
    def get_data(result):
        return result["data"]

    @staticmethod
    def get_msg(result):
        return result["msg"]


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        from decimal import Decimal
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, Decimal):
            return float(obj)
        else:
            return json.JSONEncoder.default(self, obj)


class Result:
    success_code = "0"
    fail_code = "1"

    def __init__(self):
        pass

    @staticmethod
    def success(data=[], msg="查询成功", count=-1,other=None):
        result = OmnisService.success(data=data, msg=msg, count=count,other=other)
        return json.dumps(result, cls=DateEncoder)

    @staticmethod
    def success_response(data=[], msg="查询成功", count=-1, cookies={},other=None):
        result = Result.success(data, msg, count,other)
        response = HttpResponse(result, content_type="application/json;charset=utf-8")
        for item in cookies.keys():
            response.set_cookie(item, cookies[item])
        return response

    @staticmethod
    def fail(data=[], code="1", msg=""):
        result = OmnisService.fail(data=data, code=code, msg=msg)
        return json.dumps(result, cls=DateEncoder)
        # result = {"code": code, "msg": msg, "success": False, 'data': data}
        # return json.dumps(result, cls=DateEncoder)

    @staticmethod
    def fail_response(data=[], code="1", msg="", status=200):
        result = Result.fail(data, code, msg)
        r = HttpResponse(result, content_type="application/json;charset=utf-8", status=status)
        # 为文件下载，提供数据，文件下载无法获取到内容，内容前端已经设置blob类型，所以只能靠header信息
        r.__setitem__("success", False)
        from django.utils.encoding import escape_uri_path
        msg = escape_uri_path(msg)
        r.__setitem__("msg", msg)
        return r

    @staticmethod
    def success_file_response(file_io, filename, size=0):
        from django.http import FileResponse
        from django.utils.encoding import escape_uri_path
        response = FileResponse(file_io)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Length'] = size
        response['Content-Disposition'] = 'attachment;filename={0}'.format(
            escape_uri_path(os.path.basename(filename)))
        return response

    @staticmethod
    def file_response(target_file_path, filename):
        file = open(target_file_path, 'rb')
        size = os.path.getsize(target_file_path)
        return Result.success_file_response(file, filename, size)
        # response = HttpResponse(file)
        # response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        # response['Content-Disposition'] = 'attachment;filename={filename}'.format(filename=filename)
        # return response


def get_uuid():
    import uuid
    return str(uuid.uuid4())


def sqlToData(sql, args=()):
    return connection_sql_to_data(sql, args)


def connection_sql_to_data(sql, args=(), datasource=None):
    from django.db import connections, connection
    from collect.utils.log import get_collect_log
    logger = get_collect_log()
    if datasource:
        if datasource not in connections:
            return []
        data_connection = connections[datasource]
    else:
        data_connection = connection
    with data_connection.cursor() as cursor:
        if len(args) == 0:
            cursor.execute(sql)
        else:
            from time import time
            start = time()
            cursor.execute(sql, args)
            stop = time()
            spend = stop - start
            if spend >= 3:
                logger.debug(sql)
                logger.debug(args)
                logger.debug("耗时 %s 秒,请注意优化sql" % (spend))

        def dictfetchall(cursor):
            desc = cursor.description
            return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

        result = dictfetchall(cursor)
        return result
    data_connection.close()


def executeSQLMany(sql, args=[]):
    """
    批量执行
    :param sql:
    :param args:
    :return:
    """
    from django.db import connection
    with connection.cursor() as cursor:
        if len(args) == 0:
            cursor.execute(sql)
        else:
            from time import time
            start = time()
            count = cursor.executemany(sql, args)
            stop = time()
            spend = stop - start
            if spend >= 3:
                from collect.utils.log import get_collect_log
                logger = get_collect_log()
                logger.debug(sql)
                logger.debug(args)
                logger.debug("耗时 %s 秒,请注意优化sql" % (spend))

            connection.commit()
            return count
    connection.close()


def value_check(check_list=[]):
    """
        装饰器，视图异常捕获

        :param param1: this is a first param
        :param param2: this is a second param
        :returns: 返回json格式的异常到前台
        :raises keyError: raises an exception
        @author： jhuang
        @time：08/02/2018
    """

    def wrapper(func):
        def inner_wrapper(*args, **kwargs):
            from collect.utils.log import get_collect_log
            logger = get_collect_log()

            try:
                request = list(args)[1]
                if request.method == "GET":
                    data = request.query_params.dict()
                else:
                    data = request.data
                logger.info(data)
                for item in check_list:
                    # 检查类型
                    check_type = item["check_type"]
                    # 字段名
                    name = item["name"]

                    pass_result = True
                    if check_type == "NOT_NULL" and data_value_check.not_empty(name, data):  # 为空
                        pass_result = False
                    elif check_type == "MUST_INT" and data_value_check.not_int(name, data):  # 非整形
                        pass_result = False
                    elif check_type == "MUST_INT_CAN_NULL" and data_value_check.not_int_can_null(name, data):  # 非整形
                        pass_result = False
                    elif check_type == "MUST_LIST" and data_value_check.not_list(name, data):  # 非整形
                        pass_result = False
                    elif check_type == "MUST_OBJ" and data_value_check.not_obj(name, data):  # 非整形
                        pass_result = False
                    if not pass_result:  # 检查未通过
                        return Result.fail_response(code=item["code"], msg=item["msg"])
                import time
                start = time.time()
                ret = func(*args, **kwargs)
                end = time.time()
                spend = end - start
                logger.info(" 耗时 %s 秒" % (spend))
                return ret
            except Exception as e:

                raise e

        return inner_wrapper

    return wrapper


def listToTree(arr, id, pid, child):
    r = []
    hash = {}
    for json_item in arr:
        hash[json_item[id]] = json_item

    for aVal in arr:
        parent_id = aVal[pid]
        if parent_id in hash:
            hashVP = hash[parent_id]
            if child in hashVP:
                ch = hashVP[child];
                ch.append(aVal);
                hashVP[child] = ch
            else:
                ch = []
                ch.append(aVal);
                hashVP[child] = ch
        else:
            r.append(aVal)
    return r


def is_empty(name, data, check_value=True):
    """

    :param name: 字段名
    :param data: 数据对象
    :param check_value:是否检查值
    :return:
    """
    if not check_value:
        return not (name in data)
    if name in data and (data[name] or data[name] == 0):
        return False
    else:
        return True


def get_safe_data(name, data, default_value=None):
    if name in data and data[name]:
        return data[name]
    else:
        return default_value


# 支持多级查询
def get_key(key, default_value=None, data_type="", decode_type=""):
    # type: (object, object, object) -> object
    value = props.get(key, default_value, data_type)
    if value is None:
        from collect.utils.log import get_collect_log
        logger = get_collect_log()
        logger.error(" 请检查application.properties配置，不存在：%s" % key)
    if decode_type:
        if decode_type == "try":
            try:
                value = value.decode("utf-8")
            except:

                value = value.decode("gbk")
        else:
            value = value.decode(decode_type)
    return value
