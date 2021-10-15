select a.dish_type_id,
b.server_id ,b.server_ip,b.server_busi_name,b.server_name,
c.monitor_agent_id,c.monitor_agent_group
from dish_bind a
join server_instance b on a.server_id = b.server_id
left join monitor_agent c on b.server_id = c.server_id
left join server_env env on b.server_env_id = env.server_env_id
left join sys_projects p on env.sys_project_id = p.sys_project_id
where 1=1
{% if project_code %}
    and p.project_code={{project_code}}
{% endif %}