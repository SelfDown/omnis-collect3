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

