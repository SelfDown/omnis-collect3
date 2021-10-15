 select DISTINCT
                    '' AS new_server_busi_name, k.soft_name AS soft_name,k.soft_type,k_sys_code.sys_code_text as soft_type_name,
                    CONCAT(h.project_name,'/',g.hospital_name,'/',f.server_env_name) AS assets_path,s.server_env_id,
                    s.server_name,s.server_ip,s.server_virtualization_type,b.sys_code_text as server_virtualization_type_name,c.type_text,dd.sys_code_text AS server_service_type_text,
                    dd.sys_code AS server_service_type_code,d.user_name as default_user_name,e.memory_size as memory_size_key,concat(e.memory_size,'G') AS memory_size,
                    e.disk_total_size as disk_total_size_key,concat(e.disk_total_size,'G') AS disk_total_size,
                    e.cpu_cores,e.cpu_logic_count,i.monitor_agent_id,i.operate_time AS monitor_operate_time ,
                    i.create_time AS monitor_create_time,i.agent_id,i.monitor_agent_group ,f.env_code,
                    j.sys_code_text AS fuzzy_server_os_type_name,j.property_1 as os_icon,s.server_type,i.hostid,s.server_id,s.is_actived,s.server_os,s.server_busi_name

 from  ( select s.* from server_instance s LEFT JOIN server_hardware e ON e.server_hardware_id = s.server_hardware_id
LEFT JOIN monitor_agent i ON i.server_id = s.server_id where (s.is_del != 1 OR s.is_del IS NULL)  and s.server_env_id  = {{server_env_id}} and s.is_actived != '0'  ) as s LEFT JOIN server_hardware e ON e.server_hardware_id = s.server_hardware_id
LEFT JOIN monitor_agent i ON i.server_id = s.server_id
LEFT JOIN server_env f ON f.server_env_id = s.server_env_id
LEFT JOIN sys_hospital g ON g.hospital_code = f.hospital_code
LEFT JOIN sys_projects h ON h.sys_project_id = f.sys_project_id
LEFT JOIN sys_code b ON b.sys_code = s.server_virtualization_type AND b.sys_code_type = "server_virtualization_type"
LEFT JOIN sys_server_type c ON c.sys_server_type_id = s.server_type
LEFT JOIN sys_code dd ON dd.sys_code =  s.server_service_type AND dd.sys_code_type = "server_service_type"
LEFT JOIN sys_code j ON j.sys_code = s.server_os AND j.sys_code_type ="server_os_type"
LEFT JOIN server_os_users d ON  d.server_os_users_id = s.server_os_users_id AND  d.default_user = "1"
LEFT JOIN server_install_soft k ON k.server_id = s.server_id AND k.is_main_soft = "1"
LEFT JOIN sys_code k_sys_code ON k.soft_type = k_sys_code.sys_code and k_sys_code.sys_code_type = "server_service_type" order by inet_aton(s.server_ip) asc

