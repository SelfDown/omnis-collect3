3. update_data 批量参数处理
================================================
更新数组字段
     * **foreach** 循环参数中的变量
     * **item** 循环中item 名称
     * **fields** 新增、修改字段列表

批量参数处理
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
一般用于批量新增，或者修改，比如新增ID,添加修改人，新增人


配置示例1

    .. code-block:: yaml
     :caption: index.yaml


      # 更新字段

       - key: update_data
         path: collect.service_imp.request_handlers.handlers.update_data
         class_name: UpdateData
         method: handler


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



配置示例2
没有配置item,直接取数组变量
配置了item带上参数

    .. code-block:: yaml
     :caption: index.yaml

      - key: update_data
        foreach: issues
        fields:
          - field: fixVersions
            template: fields.fixVersions
          - field: status
            template: fields.status
          - field: issuetype
            template: fields.issuetype
          - field: assignee
            template: fields.assignee
          - field: issuelinks
            template: fields.issuelinks