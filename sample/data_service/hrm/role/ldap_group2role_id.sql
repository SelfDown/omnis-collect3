select distinct role_id
from ldap_group a
left join role_ldap_group b on a.ldap_group_id = b.ldap_group_id
where
1=1
{% if ldap_name_list %}
 and a.name in ({{ldap_name_list}})
{% else %}
 and 1 != 1
{% endif %}
