1. params 处理参数
=========================================
这是个非常常用的模块，程序 **模块module** 正式执行前一些简单的校验。 **extend_param**  继承参数 和 **handler_params**  处理参数，这个三个大模块，都是来处理参数的，可根据不同情况进行配置。

params 是一个大型字典。一个三层级的字典。

1. 第一层级是请求字段，所有要处理的字段都显示第一层，没写不处理，比如username 用户名。
2. 第二层是处理规则和是否验证。有template 表示要模板处理，前端不能改，有check 表示要验证，default 表示有默认值。
3. 第三层 在check 标签下使用，验证数据是否合法，template 写jinja2 表达式，值为True 表示通过，值False 表示不通过。

可以处理任何模块的请求字段，进行参数处理，一般用于

1. 校验字段是否为空，比如用户名称不能为空
#. 进行复杂服务验证字段，可能是其他系统已经存在用户名，用户名在ldap 中已经存在
#. 请求参数填写默认值，填充创建时间、创建人ID
#. 赋值某个配置文件中的值，比如配置文件中指定服务器URL,token 什么的


1.params  公共模块
>>>>>>>>>>>>>>>>>>>>>>
配置示例

    .. code-block:: yaml
     :caption: 角色删除index.yaml

     key: user_role_delete
     name: 用户删除角色
     module: 'model_delete'
     model: UserRole
     params:
       user_id_list:
         check:
           template: "{{user_id_list|must_list}}"
           err_msg: "用户不能为空"
     filter:
       user_id__in: user_id_list


       
2.template  请求字段赋值
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
params 下字段，写template 然后写jinja2 模板语句
示例：

    .. code-block:: yaml
     :caption: 项目ID 生产UUIDindex.yaml

     key: "project_save"
     module: 'model_save'
     params:
       project_id:
         template: "{{''|uuid}}"


.. note::

   **{{''|uuid}}** ,其中uuid 自定义jinja2 模板语法。生成uuid 。专门会有一章来介绍模板自定义函数。
   怎么获取当前时间、获取配置



常用的赋值方法
  .. code-block:: yaml
     :caption: 常用赋值template 

      1. {{session_user_id}} 获取当前登录用户ID 
      2. {{""|current_date_time}} 获取当前时间 %Y-%m-%d %H:%M:%S ，举例 2021-01-16 09:00:15 
      3. {{""|current_day}} 获取当前时间 "%Y-%m-%d ，举例 2021-01-16  
      4. {{password|md5}} 获取md5 值   
      5. {{""|uuid}} 获取UUID  
      6. {{password|des}} des 加密  
      7. {{"xxx"|get_key}} 获取application.properties配置文件的 的配置  




3.default  请求字段填写默认值
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
params 下字段，写default,然后填写值
示例：

    .. code-block:: yaml
     :caption: 项目ID 生产UUIDindex.yaml

     key: "project_save"
     http: true
     module: 'model_save'
     params:
       is_delete:
         default: "0"
     model: SysProjects

4.check 校验字段
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
params 下字段，写check ,字典进行验证
示例：

.. code-block:: yaml
 :caption: 用户ID 列表index.yaml

 key: user_role_delete
 name: 用户删除角色
 module: 'model_delete'
 model: UserRole
 params:
   user_id_list:
     check:
       template: "{{user_id_list|must_list}}"
       err_msg: "用户不能为空"

check 下支持的标签
::::::::::::::::::::::::::::::::::::::::::::::::::::::::
1. template 进行模板校验，写jinja2 表达式，如果值为True 表示通过，为False 表示失败
#. err_msg 如果返回False，错误信息提示。 **支持写jinja2 语句** 
#. service 请求一个服务，结果为 service_result 判断结果。用于调用其他模块结果，进行验证
   示例：

   .. code-block:: yaml
    :caption: 检查编码是否存在
    
    key: "project_save"
    http: true
    module: 'model_save'
    params:
      project_code:
        check:
          service:
            service: project.project_query
            project_code: project_code
          template: "{{service_result|length <=0 }}"
          err_msg: "【{{project_code}}】编码已经存在"

.. note::
  service 是调用内部一个服务获取返回结果 **service_result** ，进行验证。

  举个例子：用户 **工号CBH0001** 在数据库里面已经存在，这个时候根据前台字段校验编码唯一，
  都不能准确判断，一般程序员数据库保存之前，写SQL查数据库，如果此编码有记录就报错。

  而写SQL查数据库的这个动作，我们把它配置成一个服务service，我们本身就支持sql 模块。然后check下，调用这个service，
  利用template 来判断结果

  **注意** service验证传参数，需要强指定传那些参数，不会默认将params 里面的参数都传过去，而是你指定哪个传哪个


