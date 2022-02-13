with recursive digui as
(
    SELECT * from server_env where server_env_name= 'test' and is_delete = '0'
    UNION ALL
    SELECT server_env.* from digui JOIN server_env ON digui.parent_id = server_env.server_env_id
)
select * from digui ORDER BY order_index ASC