2. excel_data
=========================================
实现excel 导入数据。将 excel文件里面数据，转请求数据。
excel 只是一种传参的形式


excel 解析数据
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


* **sheets** 是个数组，可以做支持多个sheet 页解析
* **sheet_index**  表示取第几个标签页
* **start_row**    表示从第几行开始读起
* **start_col**    表示从第几列开始算起
* **fields**       表示列对应的字段，每一列对应一个字段，key 表示字段，按照顺序来。must 表示必传，否则忽略数据
* **save_field**   解析后保存的字段


配置示例

    .. code-block:: yaml
     :caption: jira 批量导入



          # excel 解析 实现类
          - key: excel_data
            path: collect.service_imp.request_handlers.handlers.excelData
            class_name: excelData
            method: handler

          handler_params:
           - key: excel_data
             file_field: file
             sheets:
               - key: page1
                 name: "第一页"
                 sheet_index: 0
                 start_row: 2
                 start_col: 0
                 fields:
                   - key: summary
                     name: 标题
                     must: true
                   - key: description
                     name: 描述
                   - key: beans
                     name: 云豆
                   - key: componentName
                     name: 模块
                   - key: issueType
                     name: 问题类型
                   - key: duedate
                     name: 到期日
                   - key: reporter
                     name: 报告人
                   - key: assignee
                     name: 经办人
                   - key: projectKey
                     name: 空间
                     must: true
                   - key: priority
                     name: 优先级
                   - key: label
                     name: 标签
                   - key: hasScript
                     name: 是否包含脚本
                   - key: fixVersion
                     name: 修复版本
                 save_field: 'issueList'

