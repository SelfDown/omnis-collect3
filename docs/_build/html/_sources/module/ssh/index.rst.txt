7. ssh 服务器操作
=========================================
这个是模仿ansible 通过配置进行执行 shell 命令。然后在此基础上可以进行文件上传，查看服务器本地文件。
它也是流程，和service_flow 大致相同

     * 支持查看服务器本地文件
     * 支持远程文件上传
     * 支持按模板生成服务器本地文件
     * 支持服务器本地拷贝文件
     * 支持服务器本地文件夹压缩
     * 支持读取服务器本地文件夹目录
     * 支持读取服务器本地文件内容
     * 支持输入shell 命令
     * 支持配置化显示错误信息，conf/ssh_error_info.yaml 根据shell 命令返回可以，提示错误信息

默认进行ssh 连接，params传一下配置

     * **server_ip** 服务器ip
     * **user** 服务器登录用户
     * **password** 服务器登录密码
     * **port** 端口默认22
     * **timeout** 连接超时，默认15秒

    .. note::
       如果不要进行ssh 连接 ，可以在模板中设置ssh_connect: false。和params 平级

模块: ssh
>>>>>>>>>>>>>>>>>>>>>>
配置示例
这个是预览服务器本地文件

    .. code-block:: yaml
     :caption: index.yaml

       - key: target_conf_preview
         module: ssh
         http: true
         must_token: true
         check_ip: true
         params:
           timeout:
             default: 3
           password:
             template: '{{password|des("decrypt")}}'
           target_upstream_path:
             template: "{{'nginx_path'|get_key}}/{{'upstream_path'|get_key}}"
           target_router_path:
             template: "{{'nginx_path'|get_key}}/{{'router_path'|get_key}}"
         shell:
           services:
             - key: start
               type: start
               name: 开始
               next: upstream_content

             - key: upstream_content
               type: node
               name: 获取upstream 的内容
               next: router_content
               shell: 'cat {{target_upstream_path}}'
               save_field: upstream_script
               ignore_error: true
               fail: end
             - key: router_content
               type: node
               name: 获取router 的内容
               shell: 'cat {{target_router_path}}'
               save_field: router_script
               ignore_error: true
               next: end
               fail: end
             - key: end
               type: end
               name: 结束

         result_handler:
           - key: add_param
             params:
               from_field: router_script
               to_field: router_script
           - key: add_param
             params:
               from_field: upstream_script
               to_field: upstream_script



    .. note::
       shell 是整个流程控制节点，下面的services,是流程的流转配置，能完整的构建出一张流程图。未来是支持services节点json引入
       services的每个节点比包含

         * **key** 服务节点的唯一标志
         * **name** 节点描述
         * **type** 表示类型 可选 start 开始，end 结束，node 节点

       这个和service_flow 一致
       支持流程结束后，调用一个服务，一般记录日志不管成功还是失败，service_flow 也支持

       结果服务自动添加flow_msg，流程返回结果，flow_success ，流程是否成功

         .. code-block:: yaml
          :caption: index.yaml

              shell:
                finish:
                  service:
                    service: router.save_conf_log
                services:
                  - key: start
                    type: start
                    name: 开始
                    next: backup_router








配置参数
>>>>>>>>>>>>>>>>>>>>>>
这里解释节点的配置参数

1. shell
::::::::::::::::::::
执行shell 命令，结果保存到save_field 中的字段

    .. code-block:: yaml
     :caption: index.yaml

        - key: upstream_content
          type: node
          name: 获取upstream 的内容
          next: router_content
          shell: 'cat {{target_upstream_path}}'
          save_field: upstream_script
          ignore_error: true
          fail: end



2. file_content
::::::::::::::::::::
读取服务器文件内容，保存save_field 中 current_router_content

    .. code-block:: yaml
     :caption: index.yaml


        - key: current_router_content
          type: node
          name: 当前router内容
          file_content:
            file: local_router_path
          next: current_upstream_content
          fail: end
          save_field: current_router_content

3. copy
::::::::::::::::::::
上传远程文件，注意to 表示目录，如果目录不存在就创建


    .. code-block:: yaml
     :caption: index.yaml

        - key: upload_upstream
          name: 上传路由文件
          type: node
          copy:
            from: "{{local_upstream_path}}"
            to: "/tmp/conf/"
          save_field: 'upload_upstream_path'
          next: change_router_path
          fail: end

    .. note::
          如果上传文件，为了安全，请先上传到tmp 目录，然后运行cp 拷贝。否则可能文件上传一半
          失败了，服务器上源文件已经破坏，导致文件很难找回

