select * from deploy_tasklist
drop table deploy_tasklist;
CREATE TABLE `deploy_tasklist` (
  `dep_task_id` varchar(255) primary key,
  `server_id` varchar(200) ,
  `war_artifactid` varchar(300) ,
  `war_groupid` varchar(265) ,
  `global_group_id` varchar(200) ,
  `install_soft_id` varchar(200) ,
  `orderindex` int(11) ,
  `deploy_flag` varchar(10),
  `notes` varchar(1000) ,
  `server_env_id` varchar(50) ,
  `create_time` varchar(50),
  `create_user` varchar(50),
  `modify_time` varchar(50),
  `modify_user` varchar(50),
  `appstatu` varchar(500) ,
  `lastversion` varchar(100) ,
  `lastglobalgroupid` varchar(100) ,
  `deploydir` varchar(255) ,
  `appurl` varchar(255) ,
  `deploystatu` text ,
  `locked` varchar(20),
  `lastdeployver` varchar(255) ,
  `publish_req_ver` varchar(255) ,
  `war_remotefilesize` varchar(255) ,
  `war_download_percent` varchar(255),
  `war_download_complete` varchar(255) ,
  `op_user` varchar(255) ,
  `war_download_speed` ,
  `beforehand_id` varchar(255) ,
  `thread_name` varchar(200) ,
  `artifact_path` varchar(255) ,
  `artifact_md5` varchar(255) ,
  `check_war_status_code` varchar(255),
  `publishReqVer` varchar(255) ,
  `deploy_` int(11) ,
  `framework_version` ,
  `comments` varchar(6000) ,
  `stability_assurance_event_id`,
  `jboss_cli_pid` varchar(10) ,
  `jboss_cli_pid_start_time` timestamp ,
  `checkwarstatu` varchar(100) ,
  `singledep_bak_path` varchar(255),
  `ip_address` varchar(255) ,
  `domain_name` varchar(255) ,
  `domain_name_address` varchar(255) 
) 




UPDATE "user_account" SET "nick" = (CASE "user_id" WHEN %s THEN %s WHEN %s THEN %s ELSE "nick" END), "username" = (CASE "user_id" WHEN %s THEN %s ELSE "username" END) WHERE "user_id" in (%s, %s)


['f89134e0-c5b5-48b7-b69b-4ce91634b641', 'zz1', 'b2c534d5-00e6-41cb-82bf-6b699f236d42', 'zz', 'f89134e0-c5b5-48b7-b69b-4ce91634b641', 't', 'f89134e0-c5b5-48b7-b69b-4ce91634b641', 'b2c534d5-00e6-41cb-82bf-6b699f236d42']


UPDATE "user_account" SET "nick" = (CASE "user_id" WHEN %s THEN %s WHEN %s THEN %s ELSE "nick" END) WHERE "user_id" in (%s, %s)


select * from sys_war

drop table sys_war;
CREATE TABLE [sys_war](
  [war_id] varchar(50), 
  [war_groupid] varchar(200), 
  [war_artifactid] varchar(200), 
  [war_name] varchar(200), 
  [project_id] varchar(50), 
  [deploy_type] varchar(5), 
  [deploy_server_type] varchar(50), 
  [create_time] varchar(50), 
  [create_user] varchar(50), 
  [modify_time] varchar(50), 
  [modify_user] varchar(50) 
  );

select a.role_id
from user_role a
where 
a.user_id = '739ade44-7e83-48a2-8c60-9a7c1e9f3d0a'
and a.role_id not in ('common','manage')
union all
CREATE TABLE `global_conf_details` (
  `global_param_id` varchar(255) primary key,
  `global_group_id` varchar(255),
  `param_key` varchar(300) ,
  `param_value` varchar(2000),
  `param_notes` varchar(1000) ,
  `create_time` timestamp ,
  `create_user` varchar(50) ,
  `modify_time` timestamp ,
  `modify_user` varchar(50) ,
  `comments` varchar(225)
) 


CREATE TABLE `global_conf_group` (
  `global_group_id` varchar(255) primary key,
  `global_group_name` varchar(255) ,
  `global_group_notes` varchar(255) ,
  `is_delete` varchar(2),
  `server_env_id` varchar(100) ,
  `create_time` timestamp ,
  `create_user` varchar(50) ,
  `modify_time` timestamp ,
   `modify_user` varchar(50) ,
  `comments` varchar(225)
) 



select a.role_id 
from role a 
left join user_role b on a.role_id = b.role_id and b.user_id = '739ade44-7e83-48a2-8c60-9a7c1e9f3d0a'
where b.user_id is null and a.role_id in ('common','manage')

select b.user_group_name as server_user_group_name,a.* from ( 

select a.* 
from server_soft_user a 
left join server_install_soft b on a.install_soft_id = b.install_soft_id 
left join server_instance c on c.server_id = b.server_id
where 1=1 and c.is_delete = '0' and c.server_env_id = '25c7d2f3-7433-4ba2-b159-427b723ee611'


) a left join
os_user_group b on a.user_group_id = b.os_user_group_id

select a.* 
from server_install_soft a
where 1=1


select * from server_os_users

drop table os_user_group;

CREATE TABLE [os_user_group](
  [os_user_group_id] varchar(50) PRIMARY KEY, 
  [user_group_name] varchar(50), 
  [user_group_code] varchar(50), 
  [user_group_src] varchar(50), 
  [comment] VARCHAR(50));


alter table sys_war add column comments varchar(255) not null;
alter table server_instance add column cpu_speed varchar(255) ;
alter table server_instance add column disk varchar(255)
alter table server_instance add column memory varchar(255)

select * from server_instance


delete  from event_log

alter table user_account add column ldap_success varchar(2) not null;
alter table user_account add column ldap_msg varchar(500) not null;
alter table user_account add column svn_success varchar(2) not null;
alter table server_os_users add column is_default varchar(2) not null;

drop table server_os_users;
CREATE TABLE [server_os_users](
  [server_os_users_id] varchar(50) PRIMARY KEY, 
  [user_name] varchar(50), 
  [user_pwd] varchar(50), 
  [server_id] varchar(50), 
  [user_group_id] varchar(50), 
  [create_time] varchar(50), 
  [create_user] varchar(50), 
  [modify_user] varchar(50), 
  [modify_time] varchar(50));


drop table event_log;

CREATE TABLE [event_log](
  [event_id] varchar(50) PRIMARY KEY, 
  [group] varchar(50), 
  [tag] varchar(50), 
  [from_service] varchar(200) NOT NULL, 
  [to_service] varchar(200), 
  [params] varchar(4000), 
  [create_user_id] varchar(50), 
  [create_time] varchar(50), 
  [finish_time] varchar(50), 
  [success] varchar(5), 
  [result] varchar(4000), 
  [msg] varchar(4000));




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
