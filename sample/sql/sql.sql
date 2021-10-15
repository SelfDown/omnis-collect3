select distinct role_id
from ldap_group a 
left join role_ldap_group b on a.ldap_group_id = b.ldap_group_id
where a.name in ('confluence-users')

select b.sys_code_text as user_status_name,a.*
from user_account a
left join sys_code b on a.user_status = b.sys_code and b.sys_code_type = 'user_job_status'
order by create_time desc

select * from user_account 
drop table role;
drop table role_menu;

CREATE TABLE [role_menu](
  [role_menu_id] varchar(50) PRIMARY KEY, 
  [role_id] varchar(50), 
  [menu_id] varchar(50));
  
select * from role;
select * from sys_menu;
insert into role_menu(role_menu_id,role_id,menu_id) values('1','common','work_station');
insert into role_menu(role_menu_id,role_id,menu_id) values('2','common','3');
insert into role_menu(role_menu_id,role_id,menu_id) values('3','manage','sys_manage');
insert into role_menu(role_menu_id,role_id,menu_id) values('4','manage','2');
insert into role_menu(role_menu_id,role_id,menu_id) values('5','manage','4');

select * from role_menu;

select distinct a.* 
from sys_menu a
left join role_menu b on a.menu_id = b.menu_id
left join user_role c on b.role_id = c.role_id
where c.user_id = '739ade44-7e83-48a2-8c60-9a7c1e9f3d0a' 

select * from sys_menu



CREATE TABLE [role](
  [role_id] varchar(50) PRIMARY KEY, 
  [role_name] varchar(255), 
  [order_index] INT(5), 
  [role_code] varchar(50));
