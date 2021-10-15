# -*- coding: utf-8 -*-
"""
@File: ldap3_utils.py
"""
from ldap3 import Server, Connection, SUBTREE, ALL_ATTRIBUTES, ALL, MODIFY_ADD, MODIFY_REPLACE


class Ldap3Class:
    def __init__(self, ldap_host, base_dn, ldap_manager, manager_passwd):
        self.ldap_host = ldap_host
        self.base_dn = base_dn
        self.manager_dn = "cn=%s,%s" % (ldap_manager, base_dn)
        self.server = Server(ldap_host, get_info=ALL)
        self.conn = Connection(self.server, self.manager_dn, manager_passwd, auto_bind=True)
        pass

    def login(self, username, pwd):
        server = Server(self.ldap_host, get_info=ALL)
        conn = Connection(server)
        conn.bind()
        conn.search(self.base_dn, "(&(objectclass=person)(cn=%s))" % (username),
                    attributes=["sn", "givenName", "mail"])
        person = conn.entries
        print(person)

        if len(person) == 0:  # 用户不存在
            return False, []
        user = person[0]
        entry_dn = user.entry_dn

        conn = Connection(self.ldap_host, entry_dn, pwd)
        login_st = conn.bind()
        if not login_st:  # 登录验证
            return False, []
        attr_dict = user.entry_attributes_as_dict
        givenName = ""
        if len(attr_dict["givenName"]) > 0:
            givenName = attr_dict["givenName"][0]
        ch_name = ""
        if len(attr_dict["sn"]) > 0:
            ch_name = attr_dict["sn"][0]
        mail = attr_dict["mail"][0]
        if len(attr_dict["mail"]) > 0:
            mail = attr_dict["mail"][0]
        data = {"ch_name": ch_name, "givenName": givenName, "email": mail,
                "username": username}
        return True, data

    def ldap3_user_add(self, user_name, user_pwd, nick, user_id, user_ou):
        """

        :param user_name: ampeng
        :param user_pwd:
        :param nick:      彭爱民
        :param user_id:    693
        :param user_ou:   ou=cs-office,ou=users,dc=tonghe,dc=com
        :return:    True or Flase
        """

        con = self.conn
        add_dn = "uid=%s,%s" % (user_name, user_ou)
        reslut = con.add(add_dn, ['organizationalPerson', 'inetOrgPerson', 'posixAccount'], \
                         {'cn': user_name, 'sn': nick, 'userpassword': user_pwd, 'uidNumber': user_id, \
                          'gidNumber': '0', 'homeDirectory': '/opt/ftpsite/%s' % user_name, \
                          'mail': '%s@cenboomh.com' % user_name, 'uid': user_name})
        return reslut

    def ldap3_user_search(self, user_name, user_ou):

        con = self.conn
        search_dn = "uid=%s,%s" % (user_name, user_ou)
        result = con.search(search_base=search_dn,
                            search_filter='(objectClass=inetOrgPerson)',
                            search_scope=SUBTREE,
                            attributes=ALL_ATTRIBUTES, )
        return result

    def ldap3_add_user_to_group(self, cn_name, user_name, user_ou, ou_name=[]):
        """

        :param cn_name:   develops
        :param user_name:  ampeng
        :param user_ou:  ou=cs-office,ou=users,dc=tonghe,dc=com
        :param ou_name:  ou=develops,ou=nexus,dc=tonghe,dc=com
        :return:  True or False
        """

        oulist = []
        for i in ou_name:
            oulist.append('ou=%s' % i)
        user_dn = "uid=%s,%s" % (user_name, user_ou)
        try:
            con = self.conn
            group_dn = str("cn=%s,%s,%s" % (cn_name, ','.join(oulist), self.base_dn))
            con.modify(group_dn, {'uniqueMember': [(MODIFY_ADD, user_dn)]}, controls=None)
            # conn.unbind_s()
            return True
        except Exception as e:
            print("%s 添加失败，原因: %s" % (cn_name, str(e)))
            return False

    def ldap3_departure_user(self, user_info):
        con = self.conn
        user_dn = "uid=%s,%s" % (user_info["ldap_uid"], user_info["user_ou"])
        modify_info = "uid=%s" % user_info["new_ldap_uid"]
        try:
            reslult = con.modify_dn(user_dn, modify_info)
            return reslult
        except Exception as e:
            raise e

    def ldap3_mod_pass(self, user_info):
        con = self.conn
        user_dn = "uid=%s,%s" % (user_info["ldap_uid"], user_info["user_ou"])
        reslult = con.modify(user_dn,
                             {'userpassword': [MODIFY_REPLACE, [user_info["new_ldap_passwd"]]]},
                             )
        return reslult


if __name__ == '__main__':
    # test  = Ldap3Class(ldap_host="172.26.0.20", base_dn="dc=weigao,dc=com",ldap_manager="Manager",manager_passwd="RQj9Ctjgc")
    # print (test.login("zhangzhi","Wgldap_2021"))
    conn = Connection("172.26.0.20", "cn=Manager,dc=weigao,dc=com", "RQj9Ctjgc")
    conn.bind()
    d = {
        "dn": "cn=z1z,ou=users,dc=weigao,dc=com",
        "object_class": ["top", "inetOrgPerson"],
        "attributes": {
            "cn": "zz",
            "sn": "z1z",
            "userpassword": "zz@888",
            "mail": "zz@163.com",
            "mobile": "18874948657"
        }
    }
    print(conn.add(**d))
