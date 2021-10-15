select *
from sys_code
where 1=1
{% if sys_code_type %}
 and sys_code_type = {{sys_code_type}}
{% endif %}
order by order_index