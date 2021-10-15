select distinct a.*
from sys_menu a
left join role_menu b on a.menu_id = b.menu_id
left join user_role c on b.role_id = c.role_id
where c.user_id = {{user_id}}
order by a.order_index