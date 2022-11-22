9. bulk_service 批量服务
=========================================
多线程执行各个不同的服务



模块: bulk_service
>>>>>>>>>>>>>>>>>>>>>>
配置示例


    .. code-block:: yaml
     :caption: index.yaml

       - key: batch_handler_script
         module: bulk_service
         log: true
         params:
           elb_list:
             check:
               template: "{{elb_list|must}}"
               err_msg: "elb 列表数据不能为空"
         batch:
           foreach: elb_list
           item: item
           service:
             service: "nacos.target_server_conf_replace"
             conf_id: "{{item.conf_id}}"

           save_field: 'bulk_result'
         result_handler:
           - key: param2result
             params:
               field: bulk_result
           - key: new_col
             params:
               to_field:
                 - field: "name"
                   template: "{{item.name}}"
                 - field: "server_ip"
                   template: "{{item.server_ip}}"
               remove:
                 - item



    .. note::
          这个是一个批量发http 请求的示例，nacos.target_server_conf_replace 是一个服务，替换文件
          默认是将params 里面的参数，都传递过来了，实际params 里面发请求的时候，已经传了个upstream_script
          然后根据，conf_id 更新upstream_script






配置参数
>>>>>>>>>>>>>>>>>>>>>>
这里解释节点的配置参数

1. batch
::::::::::::::::::::
批量处理节点的对象，批量处理的配置，都在batch 下面




2. foreach
::::::::::::::::::::
循环列表，指定参数里面，列表取值对象


3. item
::::::::::::::::::::
循环之后item 模板，变量取值

4. service
::::::::::::::::::::
处理服务名称的对象


5. append_param
::::::::::::::::::::
是否添加全部请求参数，默认True,添加全部请求参数

6. save_field
::::::::::::::::::::
保存字段


7. max_once
::::::::::::::::::::
单次执行线程的数，默认30。防止有些服务请求，做了限制比如钉钉就限制，每秒只能请求1000个



8. append_item_param
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
将循环item的参数一次性传给服务

配置示例


    .. code-block:: yaml
     :caption: index.yaml

       - key: planning_add_bulk
         name: 批量新增发布计划
         module: bulk_service
         http: true
         params:
           planning_list:
             check:
               template: "{{planning_list|must}}"
               err_msg: 发布计划列表不能为空
         batch:
           foreach: planning_list
           item: item
           append_item_param: true
           service:
             service: release.planning_add_flow
           save_field: 'bulk_result'
         result_handler:
           - key: param2result
             params:
               field: bulk_result