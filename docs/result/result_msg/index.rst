4. 返回模板消息
=========================================


    * 可以将请求参数的字段返回出来


模块: result_msg
>>>>>>>>>>>>>>>>>>>>>>
配置示例

    .. code-block:: yaml
     :caption: index.yaml


      # 处理返回消息,实现类
      - key: result_msg
        path: collect.service_imp.result_handlers.handlers.result_msg
        class_name: ResultMsg
        method: handler



:::::::::::::::::::::::::::::::::::::::::::::
1. 字段解释


     * **template** 是模板消息字段


2. result_msg 是result_handler 的结果处理器



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

