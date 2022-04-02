5. 推送接口访问记录
=========================================


    * 针对单个接口的访问，进行推送。必须是成功返回才有推送


模块: hook
>>>>>>>>>>>>>>>>>>>>>>
配置示例

    .. code-block:: yaml
     :caption: index.yaml


      # 推送接口访问参数实现类
      # hook
      - key: hook
        path: collect.service_imp.result_handlers.handlers.hook
        class_name: Hook
        method: handler



:::::::::::::::::::::::::::::::::::::::::::::
1. 字段解释


     * **result_name** 结果转参数，参数的名称


2. hook 是result_handler 的结果处理器



     .. code-block:: yaml
      :caption: 将用户名返回

        result_handler:
          - key: hook
            params:
              result_name: service_result
              service:
                service: event.event_user_create
                from_service: "service"
                result: service_result
          - key: param2result
            params:
              field: user_role_list
          - key: result_msg
            params:
              template: "【{{username}}】创建成功！"



