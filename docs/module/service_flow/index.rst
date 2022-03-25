5. service_flow 服务流程化
=========================================
很多时候我们的接口，不只是单纯操作一张表、或者一种增、删、改、查、的动作。可能需要混合是新增、修改，或者调用其他http接口。
比如新增一个内部系统用户，同时触发ldap用户新增、企业微信用户新增。

**服务流程化** 最开始这个思路的来源，就是工作流，我们的接口能否像工作流一样，遇到某个节点完成后，会流转到下个节点。
如果节点返回不正常结束整个流程。

**service_flow** 实际上已经是个小型的工作流，目标对象就是接口，通过控制节点，将一些服务组合起来。也可以用于解析
一个很大参数，有几个不同的模块，每个模块需要做不同，新增、修改接口。比如我之前遇到的场景，需要：1添加服务器信息，2添加改服务器用户列表信息。这里就相当于有2个模块


模块: service_flow
>>>>>>>>>>>>>>>>>>>>>>
配置示例
这个是调用其他服务的示例，节点upload_file 是上传文件

    .. code-block:: yaml
     :caption: index.yaml

      - key: genConf
        module: service_flow
        http: true
        log: true
        must_token: true
        check_ip: true
        params:
          conf_id:
            check:
              template: "{{conf_id|must}}"
              err_msg: "配置文件不能空"
          show_detail:
            default: true
          to_obj:
            default: true
        handler_params:
          - key: service2field
            service:
              service: router.get_router_conf
              conf_id: conf_id
              to_obj: to_obj
              show_detail: show_detail
            save_field: conf
        flow:
          services:
            - key: start
              type: start
              name: 开始
              next: upload_file
            - key: upload_file
              type: node
              name: 上传配置文件
              service:
                service: server.conf_upload
                user: conf.username
                password: conf.password
                server_ip: conf.server_ip
                port: conf.port
                upstream: conf.upstream
                router: conf.router
              next: end
              fail: end
            - key: end
              type: end
              name: 结束
        result_handler:
          - key: result_msg
            params:
              template: "【{{conf.server_ip}}-{{conf.name}}】配置替换成功"




    .. note::
       flow 是整个流程控制节点，下面的services,是流程的流转配置，能完整的构建出一张流程图。未来是支持services节点json引入
       services的每个节点比包含

         * **key** 服务节点的唯一标志
         * **name** 节点描述
         * **type** 表示类型 可选 start 开始，end 结束，node 节点






配置参数
>>>>>>>>>>>>>>>>>>>>>>
这里解释节点的配置参数

1. next
::::::::::::::::::::
表示下个节点的位置，支持写模板语法，支持switch

    .. code-block:: yaml
     :caption: index.yaml

       services:
        - key: start
          type: start
          name: 开始
          switch:
            - case: "{{ create_ldap == '1' and user.create_ldap == '0' }}"
              name: 如果前台创建ldap ，记录时没有创建，则创建ldap
              next: create_ldap
            - case: "{{ (create_ldap == '1' and user.create_ldap == '1') and (email != user.email or role_change|length >0  ) }}"
              name: 如果邮件变化，或者角色变化更新ldap
              next: update_ldap
            - case: "{{ ( create_ldap == '0' and user.create_ldap == '1' ) or ( create_ldap== '1' and  role_id_list|length <= 0) }}"
              name: 如果前台传删除ldap,记录有ldap 删除ldap。如果是创建ldap,并且角色为0 也删除ldap
              next: remove_wechat
          next: update_user



2. fail
::::::::::::::::::::
失败的时候节点流转，流程只能失败一次，一般fail 直接指向end,如果需要回退的可以指向自己删除服务节点。
如果不能保证一定成功，就加上ignore_error: true,就会忽略错误

    .. code-block:: yaml
     :caption: index.yaml

     - key: upload_file
       type: node
       name: 上传配置文件
       service:
         service: server.conf_upload
         user: conf.username
         password: conf.password
         server_ip: conf.server_ip
         port: conf.port
         upstream: conf.upstream
         router: conf.router
       next: end
       fail: end

3. ignore_error
::::::::::::::::::::
ignore_error: true 表示忽略错误

    .. code-block:: yaml
     :caption: index.yaml

        - key: trigger_delete
          name: 删除触发器
          type: node
          service:
            service: "monitor.trigger_delete_by_trigger_id_list"
            trigger_id_list: "trigger_id_list"
          fail: end
          next: item_delete
          ignore_error: true

