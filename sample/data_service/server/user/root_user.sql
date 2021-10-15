
select  distinct a.server_id,p.project_name,
a.server_busi_name,a.server_ip,a.server_os,
b.user_name,b.user_pwd,ma.monitor_agent_id,agent_id,a.is_del,ma.hostid
from server_instance a
left join server_os_users b on a.server_id = b.server_id and b.user_name = 'root'
left join server_env c on a.server_env_id = c.server_env_id
left join sys_projects p on c.sys_project_id = p.sys_project_id
left join monitor_agent ma on ma.server_id = a.server_id
where 1=1
 {% if server_id %}
    and a.server_id  = {{server_id}}
 {% elif server_id_list %}
    and a.server_id  in  ({{server_id_list}})
 {% else %}
    and 1!=1
 {% endif %}