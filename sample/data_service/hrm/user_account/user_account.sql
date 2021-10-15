select b.sys_code_text as user_status_name,
(
    select group_concat( r.role_name)
    from user_role ur
    left join role r on ur.role_id = r.role_id
    where ur.user_id= a.user_id
) as role_names,
(
    select group_concat( ur.role_id)
    from user_role ur
    where ur.user_id= a.user_id
) as role_id_list,
a.*
from ( require("user_base.sql") ) a
left join sys_code b on a.user_status = b.sys_code and b.sys_code_type = 'user_job_status'
order by create_time desc
