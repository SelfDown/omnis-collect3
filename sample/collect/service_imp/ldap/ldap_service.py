# -*- coding: utf-8 -*-
"""
@Time: 2021/7/14 16:32
@Author: zzhang zzhang@cenboomh.com
@File: ModelUpdate.py
@desc:
"""
import json

from collect.collect_service import CollectService
from collect.utils.collect_utils import get_safe_data
from ldap3 import Server, Connection, SUBTREE, ALL_ATTRIBUTES, ALL, MODIFY_ADD, MODIFY_REPLACE


class LdapService(CollectService):
    data_json_dict = {}
    LSConst = {
        "data_json_name": "data_json",
        "connection_name": "connection",
        "result_name": "result",
        "result_field_name": "result_field",
        "entries_first_name": "entries_first",
        "entries_all_name": "entries_all",
        "ignore_status_name": "ignore_status",
        "log_name": "log"

    }

    def get_ignore_status_name(self):
        return self.LSConst["ignore_status_name"]

    def get_entries_first_name(self):
        return self.LSConst["entries_first_name"]

    def get_entries_all_name(self):
        return self.LSConst["entries_all_name"]

    def get_result_field_name(self):
        return self.LSConst["result_field_name"]

    def get_result_name(self):
        return self.LSConst["result_name"]

    def get_ldap_template(self):
        """
         获取配置的ldap 模板，必须之前 get_template_from_template
        """
        return self.ldap_template

    def set_ldap_template(self, ldap_template):
        self.ldap_template = ldap_template

    def get_connection_name(self):
        return self.LSConst["connection_name"]

    def get_data_json_name(self):
        return self.LSConst["data_json_name"]

    @staticmethod
    def get_json_content(path):
        return get_safe_data(path, LdapService.data_json_dict)

    @staticmethod
    def set_json_content(path, data_json_content):
        LdapService.data_json_dict[path] = data_json_content

    def get_data_json_config_path(self):
        data_json = get_safe_data(self.get_data_json_name(), self.template)
        if not data_json:
            self.log("没有找到"+self.get_data_json_name()+"配置文件")
        config_dir = self.get_config_dir()
        config_file = config_dir + "/" + data_json
        return config_file

    def get_data_json(self, params):
        config_file_path = self.get_data_json_config_path()
        json_content = self.get_json_content(config_file_path)
        if json_content:
            return self.success(json_content)
        data_json = get_safe_data(self.get_data_json_name(), self.template)
        data_json_result = self.get_config_file(data_json, params)
        if self.is_success(data_json_result):
            data_json_content = self.get_data(data_json_result)
            self.set_json_content(config_file_path, data_json_content)
        return data_json_result

    def __init__(self, op_user):
        CollectService.__init__(self, op_user)
        self.conn = None
        self.ldap_template = None

        pass

    def get_ldap_param(self, data_json_templ, params_result):
        from collect.service_imp.common.filters.template_tool import TemplateTool
        tool = TemplateTool(op_user=self.op_user)
        data_json = tool.render(data_json_templ, params_result)
        try:
            import json
            data_json = json.loads(data_json)
            return self.success(data_json)
        except Exception as e:
            self.log(data_json, "error")
            return self.fail(str(e) + " JSON格式有误，请检查配置")

    def get_connection(self):
        return self.conn

    def set_connection(self, conn):
        self.conn = conn

    def get_connection_from_template(self):
        ldap_template = self.get_ldap_template()
        connection_dict = get_safe_data(self.get_connection_name(), ldap_template)
        if not connection_dict:
            return self.fail("没有配置连接信息")
        connection = Connection(**connection_dict)
        try:
            login_result = connection.bind()
            if not login_result:
                return self.fail("登陆失败")
        except Exception as e:
            msg = str(e)
            if "password" in connection_dict:
                connection_dict["password"] = "*****"
            self.log(json.dumps(connection_dict))
            self.log(msg)

            return self.fail("登陆失败")
        return self.success(connection)

    def prepare(self):
        params_result = self.get_params_result()
        data_json_result = self.get_data_json(params_result)
        if not self.is_success(data_json_result):
            return data_json_result
        data_json_templ = self.get_data(data_json_result)
        data_json_result = self.get_ldap_param(data_json_templ, params_result)
        if not self.is_success(data_json_result):
            return data_json_result
        data_json = self.get_data(data_json_result)
        self.set_ldap_template(data_json)

        conn_result = self.get_connection_from_template()
        if not self.is_success(conn_result):
            return conn_result
        conn = self.get_data(conn_result)
        self.set_connection(conn)
        return self.success("成功")

    def execute(self):
        conn = self.get_connection()
        ldap_template = self.get_ldap_template()

        method = get_safe_data(self.get_method_name(), ldap_template)

        # 执行方法
        if method:
            params = get_safe_data(self.get_params_name(), ldap_template)
            if not params:
                return self.fail("ldap 模板中没有配置" + self.get_params_name())
            m = getattr(conn, method)
            try:
                can_log = get_safe_data(self.get_log_name(), ldap_template, False)
                if can_log:
                    import json
                    self.log(json.dumps(params))

                r = m(**params)
                # 是否忽略执行状态
                ignore = get_safe_data(self.get_ignore_status_name(), ldap_template, False)
                if not ignore and not r:
                    return self.fail("ldap 运行失败，请排查错误")
            except Exception as e:
                raise e
                msg = str(e)
                import json
                return self.fail("ldap运行错误" + msg + ";参数：" + json.dumps(params))
        data = []
        # 处理结果
        entries = conn.entries
        result = get_safe_data(self.get_result_name(), ldap_template)
        result_field = get_safe_data(self.get_result_field_name(), ldap_template)

        def get_entry_data(entry):
            """
            ldap 对象转json
            """
            obj = {}
            for field in result_field:
                if hasattr(entry, field):
                    val = getattr(entry, field)
                    if isinstance(val, str):
                        obj[field] = val
                    else:
                        obj[field] = val.value
            return obj

        if result and result_field and len(entries) > 0:
            # 取第一个数据
            if result == self.get_entries_first_name():
                entry = entries[0]
                data = get_entry_data(entry)
            # 取全部数据
            elif result == self.get_entries_all_name():
                for entry in entries:
                    data.append(get_entry_data(entry))

        return self.success(data)

    def execute_finish(self):
        if self.conn:
            try:
                self.conn.unbind()
            except Exception as e:
                self.log("ldap 连接关闭异常：" + str(e))

    def result(self, params=None):
        prepare_result = self.prepare()
        if not self.is_success(prepare_result):
            return prepare_result
        execute_result = self.execute()
        if not self.is_success(execute_result):
            return execute_result
        data = self.get_data(execute_result)
        self.execute_finish()
        return self.success(data=data, msg="操作成功")
