select name ,a.role_id
{% if user_id_list %}
,d.username
{% endif %}

from role_ldap_group a
left join ldap_group b on a.ldap_group_id = b.ldap_group_id

{% if user_id_list %}
left join user_role c on a.role_id = c.role_id
left join user_account d on d.user_id = c.user_id
{% endif %}


where
1=1
{% if role_id_list %}
    and a.role_id in ({{role_id_list}})
{% elif user_id_list %}
    and c.user_id in({{user_id_list}})
{% else %}
  1 !=1
{% endif %}
