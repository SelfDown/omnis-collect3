
select *
from sys_projects a
where 1=1 and is_delete = '0'
{% if project_code %}
    and a.project_code = {{project_code}}
{% endif  %}

{% if sys_project_id_list %}
    and a.sys_project_id in ({{sys_project_id_list}})
{% endif %}

{% if exclude %}
    and a.sys_project_id != {{exclude}}
{% endif %}

