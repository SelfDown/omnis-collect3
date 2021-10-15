select b.server_ip,b.server_busi_name
from server_install_soft a
left join server_instance b on a.server_id = b.server_id
where a.install_soft_id = {{install_soft_id}}