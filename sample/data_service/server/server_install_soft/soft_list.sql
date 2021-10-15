select b.server_ip
from server_install_soft a
left join server_instance b on a.server_id = b.server_id
where a.install_soft_id in ({{install_soft_id_list}})