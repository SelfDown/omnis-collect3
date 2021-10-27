select distinct require('user_normal_fields.sql')
from user_account a
{% if role_code %}
left join user_role b on a.user_id = b.user_id
left join role c on c.role_id = b.role_id
{% endif  %}
where 1=1

{% if user_id_list %}
    and   a.user_id in ( {{user_id_list}})
{% endif %}

{% if create_ldap %}
    and a.create_ldap = {{create_ldap}}
{% endif %}

{% if role_code %}
   and c.role_code = {{role_code}}
{% endif %}


{% if pagination %}
limit {{start}} ,{{size}}
{% endif %}