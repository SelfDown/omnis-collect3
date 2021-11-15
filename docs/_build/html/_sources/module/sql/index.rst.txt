SQL 模块
=========================================

sql 模块主要处理数据库查询，当然也能处理修改。
    * 主要处理各种select 数据库字段。模板语法利用jinja2
    * 数据库连接利用当前项目数据库的数据源

模块: sql
>>>>>>>>>>>>>>>>>>>>>>
配置示例

    .. code-block:: yaml
     :caption: index.yaml

     service:
       - key: "project_query"
         module: 'sql'# 执行mysql 查询
         sql_file: 'project.sql'


    sql 文件示例,使用jinja2 语法
    **特别注意** 这里的控制语句的变量，不可以作用于SQL 拼接里面的变量。
    意思是 **if else**  控制语句里面 **变量不能** 显示在 where and 这些 **SQL拼接**

    .. code-block:: python
     :caption: project.sql

     select *
     from sys_projects a
     where 1=1 and is_delete = '0'
     {% if project_code %}
        and a.project_code = {{project_code}}
     {% endif  %}

     {% if sys_project_id_list %}
        and a.sys_project_id in ({{sys_project_id_list}})
     {% endif %}

     {% if exclude %}
        and a.sys_project_id != {{exclude}}
     {% endif %}


配置参数
>>>>>>>>>>>>>>>>>>>>>>


data_source
::::::::::::::::::::
* 支持 **data_source** 切换数据源，比如系统连接zabbix 数据库。至于django项目怎么配置多个数据源，可以百度一波

    .. code-block:: yaml
     :caption: index.yaml

     service:
       - key: "zabbix_query"
         data_source: 'zabbix'
         module: 'sql'# 执行mysql 查询
         sql_file: 'project.sql'


log
::::::::::::::::::::
* 支持 **log** 输出执行预编译sql 和 参数

    .. code-block:: yaml
     :caption: index.yaml

     service:
       - key: "zabbix_query"
         log: true
         module: 'sql'# 执行mysql 查询
         sql_file: 'project.sql'


sql 参数
>>>>>>>>>>>>>>>>>>>>>>
module

SQL支持require
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
可以引入其他SQL文件

* 比如查看用户字段，查询用户SQL引入一些公共字段，防止有人写  'select * from user_account'  将账户密码也查询出来了
* 分页的时候数据的SQL和统计count 的SQL where 条件可以通用

        .. code-block:: python
         :caption: user.sql,带require 示例

         select require('user_normal_fields.sql')
         from user_account a
         where 1=1

         {% if user_id_list %}
            and   user_id in ( {{user_id_list}})
         {% endif %}

         order by create_time desc
         {% if pagination %}
         limit {{start}} ,{{size}}
         {% endif %}


        .. code-block:: python
         :caption: user_normal_fields.sql,带require 示例

         a.username,a.work_code,a.nick,a.user_id,
         a.create_time,a.modify_time,a.user_status,
         a.entry_date,a.leave_date,a.phone,email,
         a.create_ldap,a.password
