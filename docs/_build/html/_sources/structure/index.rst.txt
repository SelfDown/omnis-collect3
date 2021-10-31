系统架构
=========================================

.. figure:: ./life.png
   :width: 80%
   :align: center
   :alt: 生命周期

   接口生命周期

生命周期
----------------------
将一个请求比作流水，分别经过3个罐子处理。从上至下依次往下面流

* 执行前
* 执行中
* 执行后

其中 `【执行前】` 和 `【执行后】` 是公共的处理过程。主要是针对请求处理前数据进行检查和调整。 `【执行中】` 是特别复杂的业务模块处理

最后拿到数据结果，有可能是数据列表，也可能是个文件。返回结果给前台

执行前
>>>>>>>>>>>>>>>>>>>>>>
before_plugin
    * **params** 是针对单个字段进行处理，主要检查字段，

      + 比如用户名不能为空
      + 年龄必须在xx范围
      + 项目编码唯一
    * **handler_params** 主要针对多个参数进行处理。目前已经封装的8个处理器

      + 比如在xxx区域，客户编码唯一。要传区域ID,一个客户编码，来检验是否唯一。
      + 查询数据，作为请求参数，比如根据工号，查询用户邮箱，来进行发送邮件


执行中
>>>>>>>>>>>>>>>>>>>>>>
module
这里有相当多的业务模块，目前已经实现了15个模块。后续将详细，介绍这里以sql 模块举例

    * **sql** 处理数据库查询，根据请求参数控制执行不同的sql

      .. code-block:: yaml
         :caption: index.yaml

         service:
           - key: "project_query"
             http: true
             log: true
             module: 'sql'# 执行mysql 查询
             sql_file: 'project.sql'

      * service 表示服务节点，可以看出里面是个数组，这个文件里面可以放很多服务
      * key 表示 服务的标志
      * http 表示这个接口是否支持http 访问
      * log 表示是否输出日志
      * sql_file 表示执行的sql文件

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

      这里看到 {% if ...%} 这样的操作符，如果你对jinja2 熟悉的话，这些语法就相当清楚。
      这里就利用jinja2 进行一些SQL拼接，渲染成 **预编译语句** 然后执行。所运行这个模块你必须
      对SQL 语句编写熟悉，还有对jinja2 渲染语法了解。

      从这个sql 可以看出，这里动态拼接sql,如果有项目编码，就拼接

      and a.project_code = {{project_code}}。{{project_code}}一个占位符， 是前端传过来的project_code变量值

      .. note::
         有人可能会问，这个SQL这样拼接，会不会有SQL注入的风险，如果在project_code 里面写“; drop  database xxx”
         会不会删库？

         答案是： 不会。我渲染了2遍，渲染成预编译语句，以占位符代理原值。所以 **if 模板里面的变量不要放在 SQL执行中** 。
         为了安全，执行SQL语句的变量我都换成了占位符。可以通过params 来创造个新的变量，if控制结构就用 新变量


执行后
>>>>>>>>>>>>>>>>>>>>>>
after_plugin
    * **result_handler** 针对结果数据进行处理，主要处理msg和data，目前封装了20个数据处理器

      + 比如将部门列表数据转成树形结构
      + 将结果列表转成对象
      + 将某个字段，由字符串转成数组、或者json 对象
    * **result_tag** 这里主要模仿json-rpc协议，将前端请求传的某个比如ID字段，直接返回个前端，放在other
