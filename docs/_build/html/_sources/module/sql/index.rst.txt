1. sql 模块查询
=========================================
sql 模块主要处理数据库查询，
    * 主要处理各种select,join、group by、order 等SQL。你要你能写得出，SQL接口就能构造出来。模板语法利用jinja2 来拼接SQL
    * 数据库连接利用当前项目的数据源,一般使用django 的默认数据源,也有特殊情况需要连接其他数据库,支持数据源切换
    * 没有限制执行哪种数据库,可以是mysql、oracle、sqlite等等，主要看django系统配置的什么数据源

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

    .. note::
       意思是 **if else**  控制语句里面 **变量值的字符串操作不能** 显示在 where and 这些 **SQL拼接**
       比如 {%if project_code in ["PM"] %} and project_code = {{project_code}} {% endif %}

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


1. data_source
::::::::::::::::::::
* 支持 **data_source** 切换数据源，比如系统连接zabbix 数据库，查询最新监控项数据。至于django项目怎么配置多个数据源，可以百度一波
* 默认是 **default** 数据源，data_source 可以不写

    .. code-block:: yaml
     :caption: index.yaml

     service:
       - key: "zabbix_query"
         data_source: 'zabbix'
         module: 'sql'# 执行mysql 查询
         sql_file: 'project.sql'


2. log
::::::::::::::::::::
* 支持 **log** 输出执行预编译sql 和 参数

    .. code-block:: yaml
     :caption: index.yaml

     service:
       - key: "zabbix_query"
         log: true
         module: 'sql'# 执行mysql 查询
         sql_file: 'project.sql'

3. sql_file
::::::::::::::::::::
* 指定执行sql的文件位置

    .. code-block:: yaml
     :caption: index.yaml

     service:
       - key: "zabbix_query"
         log: true
         module: 'sql'# 执行mysql 查询
         sql_file: 'project.sql'


sql 参数
>>>>>>>>>>>>>>>>>>>>>>
sql 拼接里面的参数，这里支持jinja2 的公共语法

1. session_user_id 当前登录用户ID
:::::::::::::::::::::::::::::::::::::::::::::::::

所以前台不能传此参数

    .. code-block:: python
     :caption: 查询当前用户信息

     select *
     from user_account a
     where 1=1
     and a.user_id = {{session_user_id}}



2. 简单数组处理 in 处理
:::::::::::::::::::::::::::::::::::::::::::::::::
比如用户ID user_id
SQL 语法 in 必须是 user_id in ('a','b','c')。
前台传过来数组{'user_id_list':['a','b','c']}
在SQL模板 的写法是 user_id in ( {{user_id_list}})


        .. code-block:: python
         :caption: in 语句示例

         select require('user_normal_fields.sql')
         from user_account a
         where 1=1

         {% if user_id_list %}
            and   user_id in ( {{user_id_list}})
         {% endif %}

**不支持对象数组[{'user_id':'a'},{'user_id':'b'}]**

3. require,引入公共文件
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
可以引入其他SQL文件，路径支持相对路径。
如果是上级目录下common的xx.sql文件，则是require("../common/xx.sql") **require里面不能空格**

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


常用示例
>>>>>>>>>>>>>>>>>>>>>>


1. 用户基础查询
:::::::::::::::::::::::::::::::::::::::::::::::::::::::

    .. code-block:: python
     :caption: 查询用户列表信息

     select distinct require('user_normal_fields.sql')
     from user_account a
     {% if role_code %}
     left join user_role b on a.user_id = b.user_id
     left join role c on c.role_id = b.role_id
     {% endif  %}
     where 1=1

     {% if user_id_list %}
        and   a.user_id in ( {{user_id_list}})
     {% endif %}

     {% if create_ldap %}
        and a.create_ldap = {{create_ldap}}
     {% endif %}

     {% if role_code %}
       and c.role_code = {{role_code}}
     {% endif %}


     {% if pagination %}
     limit {{start}} ,{{size}}
     {% endif %}


2. 利用【用户基础查询】,查用户分页信息
:::::::::::::::::::::::::::::::::::::::::::::::::::
    .. code-block:: python
     :caption: 查询用户分页

     select b.sys_code_text as user_status_name,
     (
        select group_concat( r.role_name)
        from user_role ur
        left join role r on ur.role_id = r.role_id
        where ur.user_id= a.user_id
     ) as role_names,
     (
        select group_concat( ur.role_id)
        from user_role ur
        where ur.user_id= a.user_id
     ) as role_id_list,
     a.*
     from ( require("user_base.sql") ) a
     left join sys_code b on a.user_status = b.sys_code and b.sys_code_type = 'user_job_status'
     order by create_time desc


3. 利用【用户基础查询】，统计用户总数
:::::::::::::::::::::::::::::::::::::::::::::::::::
    .. code-block:: sql
     :caption: 查询用户count

     select count(*) as `count`
     from ( require("user_base.sql") ) a
