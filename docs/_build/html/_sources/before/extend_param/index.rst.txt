2. extend_param 继承参数
=========================================
extend_param 是继承params 后的一个参数处理，如果其他service 有差多类似的参数，可以直接继承。比如新增和修改，只有部分不一样，可以继承

直接指向具体服务。extend_param: dish.dish_bind

如果需要改写某个字段，直接在params里面字段。优先params里面字段，然后再extend_param继承参数

1.extend_param  公共模块
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
配置示例

    .. code-block:: yaml
     :caption: 角色删除index.yaml

     # 删除绑定面板
     - key: "dish_bind_delete"
       module: 'model_delete'# 执行监控 查询
       extend_param: dish.dish_bind
       filter:
         dish_type_id__in: dish_type_id_list
         server_id__in: server_id_list
       model: DishBind


