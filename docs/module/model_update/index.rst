3. model_update 模型修改
=========================================
model_update 主要处理记录修改
    * 主要利用django model update

模块: model_update
>>>>>>>>>>>>>>>>>>>>>>
配置示例

    .. code-block:: yaml
     :caption: 项目修改index.yaml

     key: project_update
     http: true
     module: model_update
     params:
       sys_project_id:
         check:
           template: "{{sys_project_id|must}}"
           err_msg: "项目不能为空"
       project_code:
         check:
           service:
             service: project.project_query
             project_code: project_code
             exclude: sys_project_id
           template: "{{service_result|length <=0 }}"
           err_msg: "【{{project_code}}】编码已经存在"
     model: SysProjects
     filter:
       sys_project_id: sys_project_id
     exclude_save_field: # 更新排除字段
       - sys_project_id
     result_handler:
       - key: result_msg
         params:
           template: "项目修改成功！"

    * params 节点，表示进行参数处理。比如记录编码必须唯一;类型不能为空;年龄必须是数字
    * result_hanlder 是对返回结果进行处理。比如密码隐藏

    **params 和result_handler 是公共模块**  这里不过多介绍。

    有的假 **删除** ，是更新记录的某个字段，也 **用model_update**


配置参数
>>>>>>>>>>>>>>>>>>>>>>


1. model，修改数据的模型
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::
* django 数据库对应模型对象，ORM中的model。
* 前端传过来的字段必须和model 里面的字段一一对应才能修改


.. code-block:: yaml
 :caption: index.yaml

  key: "project_update"
  name: 项目保存
  module: 'model_save'
  filter:
    sys_project_id: sys_project_id
  model: SysProjects


2. filter，过滤条件
:::::::::::::::::::::::::::::::::::
* 调用django filter 方法,比如 Blog.objects.filter(id__in = [3,6,9])
* 常用filter 方法。修改一般是等于或者in 就可以了

  1. __contains(包含)

  #. __in （其中之一，可以传入一个列表，传多个值。）

  #. __range(一个范围，使用元祖)

  #. 如果是 **等于** ，就直接字段：值,key：value


.. code-block:: yaml
 :caption: index.yaml

  key: "project_update"
  name: 项目保存
  module: 'model_save'
  filter:
    sys_project_id: sys_project_id
  model: SysProjects



3. exclude_save_field，排除字段
:::::::::::::::::::::::::::::::::::
* 有些字段不能更新，比如金额、ID ,什么的防止被恶意篡改



.. code-block:: yaml
 :caption: index.yaml

  key: "project_update"
  name: 项目保存
  module: 'model_save'
  filter:
    sys_project_id: sys_project_id
  exclude_save_field: # 更新排除字段
    - sys_project_id
  model: SysProjects



4. update_fields ，只能修改字段，不填可以更新全部字段
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
* 比如有些重要表，一些过程状态字段不能修改，而只能改页面上显示的基础字段


.. code-block:: yaml
 :caption: index.yaml

  key: "project_update"
  name: 项目保存
  module: 'model_save'
  filter:
    sys_project_id: sys_project_id
  update_fields: # 可以更新字段
    - project_code
    - project_name
  model: SysProjects



常用示例
>>>>>>>>>>>>>>>>>>>>>>


1. 項目保存
:::::::::::::::::::::::::::::::::::::::::::::::::::::::

    .. code-block:: yaml
     :caption: 保存項目信息

     key: project_update
     http: true
     module: model_update
     params:
       sys_project_id:
         check:
           template: "{{sys_project_id|must}}"
           err_msg: "项目不能为空"
       project_code:
         check:
           service:
             service: project.project_query
             project_code: project_code
             exclude: sys_project_id
           template: "{{service_result|length <=0 }}"
           err_msg: "【{{project_code}}】编码已经存在"
       modify_user:
         template: "{{session_user_id}}"
       modify_time:
         template: "{{''|current_date_time}}"
       to_obj:
         default: true
     handler_params:
       - key: service2field
         service:
           service: project.project_query
           sys_project_id: sys_project_id
           to_obj: to_obj
         save_field: project
         template: "{{ not project.sys_project_id|is_empty  }}"
         err_msg: "项目不存在"
     model: SysProjects
     filter:
       sys_project_id: sys_project_id
     update_fields: # 如果没有就更新全部
       - project_code
       - project_name
     exclude_save_field: # 更新排除字段
       - sys_project_id
     result_handler:
       - key: result_msg
         params:
           template: "项目修改成功！"

2. 項目假刪除
:::::::::::::::::::::::::::::::::::::::::::::::::::::::

    .. code-block:: yaml
     :caption: 項目假刪除

     key: project_delete
     http: true
     module: model_update
     log: true
     params:
       sys_project_id_list:
         check:
           template: "{{sys_project_id_list|must}}"
           err_msg: "项目不能为空"
       modify_user:
         template: "{{session_user_id}}"
       modify_time:
         template: "{{''|current_date_time}}"
       is_delete:
         default: "1"
     handler_params:
       - key: service2field
         service:
           service: project.project_query
           sys_project_id_list: sys_project_id_list
         save_field: project_list
         template: "{{ project_list|length >0 }}"
         err_msg: "项目不存在"
     model: SysProjects
     filter:
       sys_project_id__in: sys_project_id_list
     update_fields: # 如果没有就更新全部
       - modify_user
       - modify_time
       - is_delete
     result_handler:
       - key: result_msg
         params:
           template: "项目删除成功！"

