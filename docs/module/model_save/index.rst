2. model_save 模型保存
=========================================
model_save 主要处理单表数据单个保存
    * 主要利用django model save

模块: model_save
>>>>>>>>>>>>>>>>>>>>>>
配置示例

    .. code-block:: yaml
     :caption: 用户保存index.yaml

     key: "user_account_save"
     name: 用户保存
     module: 'model_save'
     params:
       user_id:
         check:
           template: "{{user_id|must}}"
           err_msg: "用户不能为空"
       username:
         check:
           service:
             service: hrm.get_user
             username: username
           template: "{{service_result|length<=0}}"
           err_msg: "【{{username}}】 用户名已经存在"
     model: UserAccount
     result_handler:
       - key: new_col
         params:
           to_field:
             - field: 'password'
               template: "******"


    * params 节点，表示进行参数处理。比如记录编码必须唯一;类型不能为空;年龄必须是数字
    * result_hanlder 是对返回结果进行处理。比如密码隐藏

    **params 和result_handler 是公共模块**  这里不过多介绍。
    这里指定model,表示数据库执行django 模型，在service_roueter.yml 有指定配置。

    .. note::

        比如用户表user_account 对应UserAccount。
        通过 `python manage.py inspectdb > sample/models/models.py` 生成。这里目录位置根据项目调整
        
        .. code-block:: python
         :caption: 在service_roueter.sql

         # django 模型配置
         django_model:
           # django model 文件位置
           model_file: sample.models.models



配置参数
>>>>>>>>>>>>>>>>>>>>>>


1. model
::::::::::::::::::::
* django 数据库对应模型对象，ORM中的model。
* 前端传过来的字段必须和model 里面的字段一一对应


.. code-block:: yaml
 :caption: index.yaml

  key: "user_account_save"
  name: 用户保存
  module: 'model_save'
  model: UserAccount



常用示例
>>>>>>>>>>>>>>>>>>>>>>


1. 用户保存
:::::::::::::::::::::::::::::::::::::::::::::::::::::::

    .. code-block:: yaml
     :caption: 保存用户信息

     key: "user_account_save"
     name: 用户保存
     module: 'model_save'
     must_login: false

     params:
       user_id:
         check:
           template: "{{user_id|must}}"
           err_msg: "用户不能为空"

       nick:
         check:
           template: "{{nick|must}}"
           err_msg: "昵称不能空"
       username:
         check:
           service:
             service: hrm.get_user
             username: username
           template: "{{service_result|length<=0}}"
           err_msg: "【{{username}}】 用户名已经存在"
       password:
         check:
           template: "{{password|must}}"
           err_msg: "密码不能为空"
         template: "{{password|md5}}"
       user_status:
         check:
           template: "{{user_status|must}}"
           err_msg: "用户状态不能为空"
         default: "0"
       create_user:
         template: "{{session_user_id}}"

       create_time:
         template: "{{''|current_date_time}}"

       modify_user:
         template: "{{session_user_id}}"

       modify_time:
         template: "{{''|current_date_time}}"

       create_ldap:
         default: "0"

       is_delete:
         default: "0"
     model: UserAccount
     result_handler:

       - key: new_col
         params:
           to_field:
             - field: 'password'
               template: "******"


2. 角色保存
:::::::::::::::::::::::::::::::::::::::::::::::::::
    .. code-block:: yaml
     :caption: 角色保存

     key: "user_role_save"
     name: 用户创建角色
     must_login: false
     module: 'model_save'
     params:
        user_role_id:
          template: "{{user_role_id|uuid}}"
        user_id:
          check:
            template: "{{user_id|must}}"
            err_msg: 用户不能为空
        role_id:
          check:
            template: "{{role_id|must}}"
            err_msg: "角色不能为空"
     model: UserRole

3. 项目保存
:::::::::::::::::::::::::::::::::::::::::::::::::::


    .. code-block:: yaml
     :caption: 项目保存

     key: "project_save"
     must_login: false
     module: 'model_save'
     params:
       project_id:
         template: "{{''|uuid}}"
       code:
         check:
           template: "{{code|must}}"
           err_msg: "项目编码不能为空"
       create_user:
         template: "{{session_user_id}}"
       create_time:
         template: "{{''|current_date_time}}"
       is_delete:
         default: "0"
     model: Project