8. filter_arr
=========================================
过滤数组


配置示例

    .. code-block:: yaml
     :caption: 过滤简单数组


      - key: filter_arr
        enable: "{{build_list|length >0}}"
        foreach: build_list
        item: item
        ifTemplate: "{{  'build_flow_id' in item }}"
        save_field: update_list


1.foreach
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
循环的数组

2.item
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
item 表示子对象的字段

3.ifTemplate
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
取值规则

4.field
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
二级数组取值字段

5.itemSaveName
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
二级数组转存字段



6.itemIfTemplate
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
二级数组符合条件则保存


7.fields 二级字段对象生成规则
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
template + field


配置示例.
在jira里面，从一个数组中，对象有个comments 备注列表字段，
根据一些正则规则提取，里面gitlab 地址和branch 分支，存储到对象里面gitlab_link


    .. code-block:: yaml
     :caption: 过滤数组中的数组


      - key: issues_by_version_with_gitlab
        name: 根据版本号查询issue的gitlab 地址
        module: empty
        http: true
        log: true
        params:
          fix_version:
            check:
              template: "{{fix_version|must}}"
              err_msg: 版本不能为空
          jira_addr_reg:
            default: 'a commit\|(.*)/-/commit/'
          jira_branch_reg:
            default: 'on branch \[(.*)\|http'

        handler_params:
          - key: service2field
            service:
              service: jira.search_issue_by_fix_version
              fix_versions: fix_version
              with_history: false
              with_team: false
            save_field: issues
          - key: filter_arr
            enable:  "{{issues|length >0}}"
            foreach: issues
            item: item
            ifTemplate: "{{item.comments|length >0}}"
            field: comments
            itemSaveName: gitlab_link_list
            itemIfTemplate: "{{'gitlab_url'|get_key in body}}"
            fields:
              - field: gitlab_url
                template: "{{body|reg(jira_addr_reg)}}"
              - field: gitlab_branch
                template: "{{body|reg(jira_branch_reg)}}"
        result_handler:
          - key: param2result
            params:
              field: issues