
select b.server_id,a.dish_type_id,a.name
from dish_type a
left join dish_bind b on  a.dish_type_id = b.dish_type_id
left join server_instance c on b.server_id = c.server_id
where c.server_env_id = {{server_env_id}}
