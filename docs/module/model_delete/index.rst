4. model_delete 模型删除
=========================================
model_delete 主要处理记录物理删除
    * 主要利用django model delete

模块: model_delete
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

    * params 节点，表示进行参数处理。比如记录编码必须唯一;类型不能为空;年龄必须是数字
    **params 和result_handler 是公共模块**  这里不过多介绍。

    有的假 **删除** ，是更新记录的某个字段，也 **用model_update**


配置参数
>>>>>>>>>>>>>>>>>>>>>>


1. model，删除数据的模型
::::::::::::::::::::
* django 数据库对应模型对象，ORM中的model。
* 前端传过来的字段必须和model 里面的字段一一对应才能修改


.. code-block:: yaml
 :caption: index.yaml

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

2. filter，过滤条件
:::::::::::::::::::::::::::::::::::
* 调用django filter 方法,比如 Blog.objects.filter(id__in = [3,6,9])
* 常用filter 方法。删除一般是等于或者in 就可以了

  1. __contains(包含)

  #. __in （其中之一，可以传入一个列表，传多个值。）

  #. __range(一个范围，使用元祖)

  #. 如果是 **等于** ，就直接字段：值,key：value


.. code-block:: yaml
 :caption: index.yaml

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





常用示例
>>>>>>>>>>>>>>>>>>>>>>


1. 用户删除
:::::::::::::::::::::::::::::::::::::::::::::::::::::::

    .. code-block:: yaml
     :caption: 保存項目信息


     key: "user_account_delete"
     name: 用户删除
     module: model_delete
     model: UserAccount
     params:
       user_id_list:
         check:
           template: "{{user_id_list|must_list}}"
           err_msg: "用户列表不能为空"
     filter:
       user_id__in: user_id_list

2. 角色删除
:::::::::::::::::::::::::::::::::::::::::::::::::::::::

    .. code-block:: yaml
     :caption: 根据用户删除角色

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

