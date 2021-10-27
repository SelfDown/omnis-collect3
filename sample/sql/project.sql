alter table user_account add column ldap_success varchar(2) not null;
alter table user_account add column ldap_msg varchar(500) not null;
alter table user_account add column svn_success varchar(2) not null;
alter table user_account add column svn_msg varchar(500) not null;




select * from user_account order by create_time desc  limit 1

select * from event

select * from server_instance

CREATE TABLE `server_instance` (
  `server_id` varchar(255)PRIMARY KEY,
  `server_env_id` varchar(200) NOT NULL,
  `sys_project_id` varchar(50) NOT NULL,
  `server_ip` varchar(300) NOT NULL,
  `server_busi_name` varchar(255) not NULL,
  `server_name` varchar(255) DEFAULT NULL,
  `server_port` varchar(300) NOT NULL,
  `server_statu` varchar(10) DEFAULT NULL ,
  `server_type` varchar(255) DEFAULT NULL ,
  `server_os` varchar(255) DEFAULT NULL ,
  `comments` varchar(225) DEFAULT NULL ,
  `is_delete` varchar(2) DEFAULT NULL,
  `create_time` timestamp NOT NULL ,
  `modify_time` timestamp NOT NULL ,
  `create_user` varchar(255),
  `modify_user` varchar(255)
) 



drop table server_env;
CREATE TABLE `server_env` (
  `server_env_id` varchar(50) PRIMARY KEY,
  `server_env_name` varchar(255) DEFAULT NULL,
  `is_hospital` varchar(2) default null,
  `hospital_code` varchar(255) DEFAULT NULL,
  `env_code` varchar(255) DEFAULT NULL,
  `env_type` varchar(255) DEFAULT NULL,
  `is_delete` varchar(2) DEFAULT NULL ,
  `leader` varchar(255) DEFAULT NULL,
  `leader_tel` char(50) DEFAULT NULL,
  `sys_project_id` varchar(100) DEFAULT NULL ,
  `parent_id` varchar(100) DEFAULT '0' ,
  `comments` varchar(225) DEFAULT NULL ,
  `order_index` int(11) DEFAULT '0',
  `create_time` timestamp NOT NULL ,
  `modify_time` timestamp NOT NULL ,
  `create_user` varchar(50) NOT NULL ,
  `modify_user` varchar(50) NOT NULL               
  
) 
select * from server_env where is_delete = '0'

select* from sys_projects

select * 
from server_env
where is_delete = '0'








select b.sys_code_text as user_status_name,a.*
from user_account a
left join sys_code b on a.user_status = b.sys_code and b.sys_code_type = 'user_job_status'
order by create_time desc

select * from user_account 
select * from sys_projects


select * from role_menu

insert into role_menu values(5,"common","common");
insert into role_menu values(6,"common","common_inner");
insert into role_menu values(7,"common","common_jira");
insert into role_menu values(8,"common","common_confluence");
insert into role_menu values(9,"common","common_gitlab");
insert into role_menu values(10,"common","common_nexus");
insert into role_menu values(11,"common","common_jenkins");
insert into role_menu values(12,"common","common_svn");
insert into role_menu values(13,"common","common_yzj");



common	常用	0		0	100			inner
common_inner	内部应用	0		common	10			inner
common_jira	jira	1	http://172.26.0.16:8080/	common_inner	1			outer
common_confluence 	confluence	1	http://172.26.0.17:8090 	common_inner	10			outer
common_gitlab	gitlab	1	http://172.26.0.18/	common_inner	20			outer
common_nexus	nexus	1	http://172.26.0.19:8081/	common_inner	30			outer
common_jenkins	jekins	1	http://172.26.0.21:8080/	common_inner	40			outer
common_svn	svn	1	http://172.26.0.20:3343/	common_inner	50			outer
common_yzj	云之家	1	https://im.weigaoholding.com/home/	common_inner	60			outer



drop table role;



CREATE TABLE [role](
  [role_id] varchar(50) PRIMARY KEY, 
  [role_name] varchar(255), 
  [order_index] INT(5), 
  [role_code] varchar(50));
  
  
  
  
  
CREATE TABLE `sys_projects` (
  `sys_project_id` varchar(100) PRIMARY KEY,
  `project_name` varchar(1000) DEFAULT NULL,
  `project_code` varchar(100) DEFAULT NULL,
  `create_time` timestamp ,
  `modify_time` timestamp ,
  `create_user` varchar(50),
  `modify_user` varchar(50),
  `comments` varchar(225) DEFAULT NULL ,  
  `is_delete` char(50) DEFAULT NULL,
  `order_index` int(11) DEFAULT NULL
) 
