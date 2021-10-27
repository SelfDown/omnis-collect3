select require('user_normal_fields.sql'),


(
    select group_concat( r.role_name)
    from user_role ur
    left join role r on ur.role_id = r.role_id
    where ur.user_id= a.user_id
) as role_names


from user_account a
where
1=1
{% if username %}
    and a.username = {{username}}
{% endif %}
{% if user_id %}
    and a.user_id = {{user_id}}
{% endif %}
{% if exclude_user_id %}
    and a.user_id != {{exclude_user_id}}
{% endif %}
{% if password %}
   and a.password = {{password}}
{% endif %}






limit 1