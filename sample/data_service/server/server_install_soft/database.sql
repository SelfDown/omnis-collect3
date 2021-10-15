 select
         b.server_name, b.server_ip, c.server_env_id, c.server_env_name, d.hospital_code, d.hospital_name,
        e.sys_project_id , e.project_name, e.project_code,
        CONCAT_WS("/",c.server_env_name,d.hospital_name,e.project_name) as env_info,
        CONCAT_WS("/",b.server_ip,a.db_schema) as db_info,
        c.env_code,
        a.*

from (

        SELECT DISTINCT
            a.*,
            FALSE AS visitor,
            FALSE AS normal,
            FALSE AS dba,
            FALSE AS senior,
            FALSE AS visitor_disabled,
            FALSE AS normal_disabled,
            FALSE AS dba_disabled,
            FALSE AS senior_disabled
        FROM
            server_install_soft a
            JOIN server_instance b ON a.server_id = b.server_id
            AND ifnull( b.is_del, '0' ) = '0'
            LEFT JOIN server_env c ON b.server_env_id = c.server_env_id
            left join sys_projects p on c.sys_project_id = p.sys_project_id
        WHERE
            1 = 1
            AND a.soft_type IN ( {{soft_type}} )
            AND p.project_code= {{project_code}}
	)

	as a


join server_instance b on a.server_id = b.server_id  and ifnull(b.is_del,'0') = '0'
left join server_env c on b.server_env_id = c.server_env_id
LEFT JOIN sys_hospital d ON d.hospital_code = c.hospital_code
left join sys_projects e on c.sys_project_id = e.sys_project_id