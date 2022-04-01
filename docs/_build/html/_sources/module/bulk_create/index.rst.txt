8. bulk_create 批量新增
=========================================
基于django 的模型批量新增，用于数据批量新增。也有bulk_update ，批量修改



模块: bulk_create
>>>>>>>>>>>>>>>>>>>>>>
配置示例
这个是调用其他服务的示例，节点upload_file 是上传文件

    .. code-block:: yaml
     :caption: index.yaml

       - key: jira_op_log_save
         module: 'bulk_create'
         model: JiraOpLog
         params:
           bulk_result:
             check:
               template: "{{ bulk_result |must }}"
               err_msg: "结果不能为空"
             default: []
         handler_params:
           - key: update_data
             name: 修改数据
             foreach: bulk_result
             item: item
             fields:
               - field: jira_log_id
                 template: "{{''|uuid}}"
               - field: create_user
                 template: "{{session_user_id}}"
               - field: create_time
                 template: "{{''|current_date_time}}"
               - field: op
                 template: "import"
               - field: project_key
                 template: "{{item.item.projectKey}}"
               - field: summary
                 template: "{{item.item.summary}}"
               - field: description
                 template: "{{item.item.description}}"
               - field: label
                 template: "{{item.item.label}}"
               - field: assignee
                 template: "{{item.item.assignee}}"
               - field: component_name
                 template: "{{item.item.componentName}}"
               - field: fix_version
                 template: "{{item.item.fixVersion}}"
               - field: reporter
                 template: "{{item.item.reporter}}"
               - field: priority
                 template: "{{item.item.priority}}"
               - field: issue_type
                 template: "{{item.item.issueType}}"
               - field: has_script
                 template: "{{item.item.hasScript}}"
               - field: duedate
                 template: "{{item.item.duedate}}"
               - field: beans
                 template: "{{item.item.beans}}"
               - field: issue_key
                 template: "{{item.data.key|safe}}"
               - field: msg
                 template: "{{item.msg|substr(0,1500)}}"


         model_field: 'bulk_result' # 模型字段保存位置



    .. note::
       handler_params 是处理请求参数，update_data 是修改数据






配置参数
>>>>>>>>>>>>>>>>>>>>>>
这里解释节点的配置参数

1. model_field
::::::::::::::::::::
表示取参数中哪个字段，作为批量新增的参数


    .. code-block:: yaml
     :caption: index.yaml

       model_field: 'bulk_result' # 模型字段保存位置

2. model
::::::::::::::::::::
django 里面的模型


    .. code-block:: yaml
     :caption: index.yaml

       model: JiraOpLog

