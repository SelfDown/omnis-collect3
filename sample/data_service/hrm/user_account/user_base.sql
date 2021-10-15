select require('user_normal_fields.sql')
from user_account
where 1=1

{% if user_id_list %}
    and   user_id in ( {{user_id_list}})
{% endif %}

{% if pagination %}
limit {{start}} ,{{size}}
{% endif %}