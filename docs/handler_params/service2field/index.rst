1. servic2field 
=========================================
服务转字段，将整体一个服务，一般是查询服务，比如查询用户作为某一个字段，然后获取改字段作为一个参数

服务转字段
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


* template 结果为True 表示正常。为False表示异常
* err_msg  结果异常时，错误提示信息
* **注意** 这里的参数，是传多少接受多少，默认不会传全部数据
* **注意** 如果需要数组变量、boolean 、数字变量，请在params 中定义好，默认使用字符串
* 直接2级定位参数中的变量，假设请求参数有user 对象 。里面{"name":"张三"}。可以这么**user.name** 获取到 “张三” 字符串。支持一级同理，user 就是传对象



配置示例

    .. code-block:: yaml
     :caption: 角色删除index.yaml


      # 服务转字段 实现类
        - key: service2field
          path: collect.service_imp.request_handlers.handlers.service2field
          class_name: Service2Field
          method: handler

     # 获取项目信息

      handler_params:
        - key: service2field # 获取项目信息
          service:
            service: 'jira.projectInfo'
            projectKey: "projectKey"
            username: username
            password: password
          save_field: 'projectInfo'
          template: "{{projectInfo.id}}"
          err_msg: "【{{projectKey}}】项目不存在"

      # 获取服务器用户
      # 获取日志路径    
      handler_params:
        - key: service2field
          service:
            service: 'release.applicationServerInfo'
            dep_task_id: dep_task_id
          save_field: 'serverUser'
          template: "{%if serverUser.user_name %} True {% else %} False {% endif %}"
          err_msg: "{{serverUser.server_ip}} 没有配置 root 用户"
        - key: service2field
          service:
            service: 'release.applicationLogPath'
            dep_task_id: dep_task_id
          save_field: 'serverLog'
          template: "{%if serverLog.path %} True {% else %} False {% endif %}"
          err_msg: "{{serverUser.server_ip}} 没有配置 日志路径"   


        - key: "oracle_item_delay_delete"
          module: 'monitor'# 执行监控 查询
          params:
            install_soft_id_list:
              check:
                template: "{{ install_soft_id_list |must_list }}"
                err_msg: "软件列表不能为空！"
                name: 软件列表
          handler_params:
            - key: service2field # 获取天览拨测主机
              service:
                service: 'monitor.monitor_server_get'
              save_field: 'monitor_server'
            - key: service2field # 根据软件ID 转成主机的keys
              service:
                service: 'server.soft_list'
                install_soft_id_list: "install_soft_id_list"
              save_field: 'server_keys'
            - key: service2field # 根据keys 转items
              service:
                service: 'monitor.key2item_ids'
                hostid: "{{monitor_server.hostid}}"
                keys: "server_keys"
              save_field: 'itemid_list'
              template: "{{itemid_list|length >0}}"
              err_msg: "软件监控项不存在"

          must_login: false
          data_json: oracle_delay_delete.json
          log: true


          
        - key: stop
          http: true
          name: 终止
          module: http
          handler_params:
            - key: service2field
              service:
                service: hrm.currentUser
              save_field: currentUser
          data_json: stop.json
          success: "{% if statu %}True{% endif %}"
          err_msg: msg
           

